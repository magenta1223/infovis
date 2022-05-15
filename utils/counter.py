import numpy as np
from pokemon.serializers import PokemonRetrieveSerializer


# 두 포켓몬을 받아서
# 각각 상대에 대한 최적의 기술을 고름
# 그리고 2턴간의 모의 배틀을 진행
# 만약 2턴 안에 승부가 가려지면서, 한쪽의 체력이 20%이상 남으면 카운터

# main problem: 최적의 기술 찾기
# 모든 move에 대해 탐색을 한다 > 결정력 계산 > 기술 기본 결정력 x 상성 계수
# 서로 사용할 기술을 정한다
# 상대방의 내구력에 따라 달라짐. 



# subproblem : 상대 내구력 대비 최적의 기술을 계산해봅시다
# 엄청 연산량이 많을 것 같은데
# 내 기술별 기본 결정력(stat * power * typeBoost)이 있고, 여기에 상성 결정력을 곱함 : Done
# 상대의 물리/특수 내구력 대비 비율이 가장 큰 기술을 고르면 됨 > matrix broad multiplication을 통해 argmax 찾음
# 그게 나의 기술
# 마찬가지로 상대도 같은 방식으로 기술을 고름

# scenario 를 좀 가정합시다
# 1) 상대방이 뭐가 나올지 모른다 > standard 기준으로 진행
# 개체값 0, 노력치 0, 레벨 50
#  
from .crawl_funcs import getRelations
from pokemon.serializers import *
from pokemon.models import *
from utils.crawl_funcs import getRelations
from django.shortcuts import get_object_or_404

DMGRELATIONS = getRelations()

def calcValues(pokemon):
    values = {
        'hp' : pokemon['hp'] + 60,
        'attack' : pokemon['attack'] + 5,
        'defense' : pokemon['defense'] + 5,
        'spattack' : pokemon['spattack'] + 5,
        'spdefense' : pokemon['spdefense'] + 5,
        'speed' : pokemon['speed'] + 5,
    }
    return values

def movePower(pokemon):
    """
    Caculate the move power
    """
    if pokemon['attack'] >= pokemon['spattack']:
        return pokemon['attack'] * 120 * 1.5 # 자속 120으로 때려박음
    else:
        return pokemon['spattack'] * 120 * 1.5 # 


def typeCoef(moveType, targetTypes):
    rel = DMGRELATIONS[moveType]['inv_rel']['offense']
    rel_coef = [ rel[t] if rel.get(t, False) else 1  for t in   targetTypes  ]
    return np.prod(rel_coef)

def defenseValue(pokemon, targetMoveType = False):
    values = calcValues(pokemon)
    
    if targetMoveType:
        if targetMoveType == "physical":
            return values['hp'] * values['defense'] / 0.411
        else:
            return values['hp'] * values['spdefense'] / 0.411
    else:
        return values['hp'] * values['defense'] / 0.411, values['hp'] * values['spdefense'] / 0.411



def findOptimalMove(actor, target):
    """
    actor : offense
    target : defense
    """
    
    actorTypes = [ str(t['type_index'])  for t in actor['types']]
    targetTypes = [ str(t['type_index'])  for t in target['types']] # json's key is always string
    target_defense, target_spdefense = defenseValue(target)
    best_coef = 0
    typecoef = ""
    for atype in actorTypes:
        typecoef = typeCoef(atype, targetTypes)
        movepower = movePower(actor) * typecoef


        if actor['attack'] >= actor['spattack']:
            movepower = actor['attack'] * 120 * 1.5 # 자속 120으로 때려박음
            coef = movepower / target_defense
        else:
            movepower = actor['spattack'] * 120 * 1.5 # 
            coef = movepower / target_spdefense
        # 뭘 만날지 모르는 상태
        # 그냥 standard setting
        # 그런게 있을지 없을지는 모르지만 일단 제일 세게 때리고 보자
        # 그리고 보통 주 공격 스탯이 더 높은 경우 그걸 채용함
        # 굳이 변태같은 플레이를 상정하지는 말자
        if coef > best_coef:
            best_coef = coef

    return best_coef

def battleSimulation(actor, target):
 
    # 상대에게 가할 수 있는 최고의 기술을 찾음
    # 물론 해당 기술을 안 배웠을 수도 있지만.. 아무튼간에 
    # 이론 상 이길 수 있냐 정도로..
    # 실제 배틀은 훨씬 복잡함. 
    # 치명타확률, 선공기, 풀죽기, 특성, 도구, 필드효과, 성격, 노력치, 개체값 등 ...
    # 물론 계산할 수 는 있음. 그러나 새로운 정보의 "탐색"에 초점을 맞춘 것. 내가 ~~~한 기술배치 쟤가 ~한 기술배치에 무슨 도구에 어쩌고 저쩌고
    # 수백만개의 경우가 나오고 컴퓨터 터진다. 
    # 그래서 가장 심플한 방법을 사용
    # 배운 기술 중 이 아니고, 자속 위력 120으로 때려박자
    # 
    aBest_coef = findOptimalMove(actor, target)
    tBest_coef = findOptimalMove(target, actor)

    # 이렇게 하지말고

    # 원래는 공격상성 / 방어상성 뭐 이런걸로 했는데
    # 공격상성불리가 뭔 의미임! 그냥 피가 안다는건데
    # 무조건 방어상성으로 간다

    # 우선 최종진화체만을 기준으로 함
    # 배틀 시뮬레이션을 해본다

    # 지진에 카운터 맞는 경우면 사실 모든게 카운터긴 함. 
    # 그런 식이면 굉장히 곤란.. 그러면 뭐 비행 아니면 카운터가 넘쳐날걸
    # 무조건 1타를 기준으로 하자. 난수1타도 안됨. 운에 의한 요소 없이도 반드시 잡을 수 있다. 
    # 1.2 이상

    counter_factor = 1.2

    # 보수적인 기준에서 카운터를 계산함 
    # 상대는 난수 1타여도 킬 인정
    # 나는 확정 1타일 때만 인정
    if actor['speed'] > target['speed']:
        # 확정 1타로 잡음
        if aBest_coef >= counter_factor:
            return 0 
        # 난수 1타에 죽을수도 있음. 카운터
        elif tBest_coef >= 0.9:
            return tBest_coef
        # 서로 1타는 아님
        else:
            return 0
    else:
        # 내가 먼저 맞는 경우 난수1타면 카운터
        if tBest_coef >= 0.9:
            return tBest_coef
        elif aBest_coef >= counter_factor:
            return 0
        else:
            return 0
      

    # 이제 스피드에 따라서 임의로 배틀
    # 을 하는데? 실제 돌리는거 말고 로직이 있지 않을까?
    # 어쩔 수 없다. 1번에 끝날지 안끝날지 안돌리고 어케암 ㅋㅋ
    # 이렇게 모든 target pokemon에 대해서 찾고
    # 그리고 stacked radial bar를 왜 씀?
    # 얼마나 불리한지를 계수로 뽑아야 함
    # 결정력 / 내구력 비율로 합시다
    # 설명 text도 넣어주면 좋겠네용

    