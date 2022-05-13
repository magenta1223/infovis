import numpy as np

from infovis.final.config.pokemon.serializers import PokemonRetrieveSerializer


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
from pokemon.serailizers import *
from pokemon.models import *

from crawl_funcs import getRelations

import os

os.chdir('C:/HW/infovis/final\config')

from utils.crawl_funcs import getRelations


from pokemon.serializers import *
from pokemon.models import *
from django.shortcuts import get_object_or_404

actor = get_object_or_404(Pokemon, pk = 1)
target = get_object_or_404(Pokemon, pk = 3)

actor = PokemonRetrieveSerializer(actor).data
target = PokemonRetrieveSerializer(target).data

actorTypes = [ str(t['type_index'])  for t in actor['types']]
targetTypes = [ str(t['type_index'])  for t in target['types']]

DMGRELATIONS = getRelations()

a1 = str(actorTypes[0]['type_index'])

def TypeCoef(actorType, targetTypes):
    rel = DMGRELATIONS[actorType]['inv_rel']['offense']
    rel_coef = [ rel[t] if rel.get(t, False) else 1  for t in   targetTypes  ]
    return np.prod(rel_coef)


DMGRELATIONS[a1]

# speed를 비교해 서로의 내구력에서 결정력을 뺌


def calcValues(pokemon):
    values = {
        'hp' : pokemon.hp + 60,
        'attack' : pokemon.attack + 5,
        'defense' : pokemon.defense + 5,
        'spattack' : pokemon.spattack + 5,
        'spdefense' : pokemon.spdefense + 5,
        'speed' : pokemon.speed + 5,
    }

    return values


def movePower(pokemon, move):
    """
    Caculate the move power
    """

    if move.dmg_cls == "":
        return pokemon['attack'] * move['power']
    else:
        return pokemon['spattack'] * move['power']


def typeCoef(moveType, targetTypes):
    rel = DMGRELATIONS[moveType]['inv_rel']['offense']
    rel_coef = [ rel[t] if rel.get(t, False) else 1  for t in   targetTypes  ]
    return np.prod(rel_coef)

def defenseValue(pokemon):
    values = calcValues(pokemon)
    return values['hp'] * values['defense'] / 0.411, values['hp'] * values['spdefense'] / 0.411






def findOptimalMove(actor, target):
    """
    actor : offense
    target : defense
    """
    actorTypes = [ t['type_index']  for t in actor['types']]
    targetTypes = [ str(t['type_index'])  for t in target['types']] # json's key is always string

    actorMoves = actor['pokemove']
    target_defense, target_spdefense = defenseValue(target)
    
    best_coef = 0
    best_power = 0
    moveType = ""
    for move in actorMoves:
        move = move['move']
        typecoef = TypeCoef(str(move['type']), targetTypes)
        movepower = movePower(actor, move) * typecoef
        if move['type']['type_index'] in actorTypes: 
            movepower *= 1.1
        # actor type과 move type 비교해서 typeBoost를 구해서 추가로 곱함
        if move['type'] == "special":
            coef = movepower / target_spdefense
        elif move['type'] == "physical": 
            coef = movepower / target_defense
        else:
            continue

        if coef > best_coef:
            best_coef = coef
            best_power = movepower
            moveType = move['type']

    return best_power, moveType

def battleSimulation(actor, target):
    actor = PokemonRetrieveSerializer(actor).data
    target = PokemonRetrieveSerializer(target).data

    actor_defense, actor_spdefense = defenseValue(actor)
    target_defense, target_spdefense = defenseValue(target)
    aPower, aType = findOptimalMove(actor, target)
    tPower, tType = findOptimalMove(target, actor)

    # 이제 스피드에 따라서 임의로 배틀
    # 을 하는데? 실제 돌리는거 말고 로직이 있지 않을까?
    # 어쩔 수 없다. 1번에 끝날지 안끝날지 안돌리고 어케암 ㅋㅋ
    # 이렇게 모든 target pokemon에 대해서 찾고
    # 그리고 stacked radial bar를 왜 씀?
    # 얼마나 불리한지를 계수로 뽑아야 함
    # 결정력 / 내구력 비율로 합시다
    # 설명 text도 넣어주면 좋겠네용

    