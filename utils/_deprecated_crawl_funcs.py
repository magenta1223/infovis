import requests
import json
import pandas as pd
import time
import os
import pickle
import numpy as np
from collections import deque


# BASE_DIR = "C:/HW/infovis/final/config"
# os.chdir(BASE_DIR)


GENERATION_DICT = {
    'generation-i' : 1,
    'generation-ii' : 2,
    'generation-iii' : 3,
    'generation-iv' : 4,
    'generation-v' : 5,
    'generation-vi' : 6,
    'generation-vii' : 7,
    'generation-viii' : 8,
}



locales = ['en', 'ko']


# TODO 
# 1. 데이터 크롤링

## 1) 세대 별 데이터셋
## - 모든 상호작용은 같은 세대안에서만 일어남
## 2) DB로 구축. 
## 3) 한국어 / 영어

# 2. 백엔드 서버 구축 (DRF)
# 3. 프론트

# 1) 백엔드 서버 구축


def get_inform(url):
    """
    get information as json from api endpoint (url) 
    """
    return json.loads(requests.get(url).content)



def crwalPokemons():
    """
    Crawl key attributes of pokemons by generations
    """
    
    # make dirs
    if not os.path.exists(f'./data'):
        os.makedirs('./data')
    
    # initialize
    poke_df = []
    move_df = []

    for generation in range(1, 9):
        # get pokemons added newly at the generation 
        pokemons = get_inform(f'https://pokeapi.co/api/v2/generation/{generation}/')

        # preprocess
        ## pokemons
        _poke_df = pd.DataFrame(pokemons['pokemon_species'])
        _poke_df['pokedex_index'] = _poke_df['url'].apply(lambda x: int(x.split('/')[-2]))
        _poke_df = _poke_df.sort_values('pokedex_index').reset_index(drop = True)
        _poke_df['generations'] = generation
        ## moves
        _move_df = pd.DataFrame(pokemons['moves'])
        _move_df['move_index'] = _move_df['url'].apply(lambda x: int(x.split('/')[-2]))
        _move_df = _move_df.sort_values('move_index').reset_index(drop = True)
        _move_df['generations'] = generation


        # acummulate
        poke_df.append(_poke_df)
        move_df.append(_move_df)
        
        # make dirs for the generation
        if not os.path.exists(f'./data/generation-{generation}'):
            os.makedirs(f'./data/generation-{generation}')
        
        # save the pokemons accumulated upto this generation  as csv 
        pd.concat(poke_df, axis = 0).to_csv(f'./data/generation-{generation}/pokemons.csv', index = False)
        pd.concat(move_df, axis = 0).to_csv(f'./data/generation-{generation}/moves.csv', index = False)
        
        # for stable crawling
        time.sleep(1)


def crawlGenerations():
    """
    Crawl generation - version, version-groups - version hierarchies
    """

    generations = {}
    version_groups = {}
    
    # all version groups
    for version in range(1, 21):
        # version group
        version_group = get_inform(f'https://pokeapi.co/api/v2/version-group/{version}')
        
        # generation of the version group
        generation = int(version_group['generation']['url'].split('/')[-2])
        
        # all versions which belongs to the version group
        versions = [ v['name'] for v in version_group['versions']]
        
        # all  
        version_groups[version_group['name']] = [ v['name'] for v in version_group['versions']]

        if generations.get(generation, False):
            # if the generation already exists, merging versions with existing ones
            generations[generation] = generations[generation].union(set(versions))
        else:
            # initialize 
            generations[generation] = set(versions)

        time.sleep(1)
    
    # 
    for g, vs in generations.items():
        generations[g] = list(vs)
    
    # save 
    with open('./data/generations.json', 'w') as f:
        json.dump(generations, f)
    with open('./data/versiongroups.json', 'w') as f:
        json.dump(version_groups, f)

# def crawlVersionGroups():
#     vg_dict = {}
#     for vg in range(1, 21):
#         versiongroup = get_inform(f'https://pokeapi.co/api/v2/version-group/{vg}/')
#         vg_dict[versiongroup['name']] = [ v['name'] for v in versiongroup['versions']]
#         time.sleep(1)
    
#     with open('./data/versiongroups.json', 'w') as f:
#         json.dump(vg_dict, f)



def crawlTypes():
    """
    Crawl All Types
    """
    
    # initialize
    types = { generation : {} for generation in range(1, 9)}

    
    for i in range(1, 19):

        # type data
        type_data = get_inform(f'https://pokeapi.co/api/v2/type/{i}')
        
        # type names
        type_names = get_names(type_data)

        # damage relation & generation pairs
        dmg_relations = [ [dmg_rel['damage_relations'], GENERATION_DICT[dmg_rel['generation']['name']]] for dmg_rel in  type_data['past_damage_relations']]
        dmg_relations.append([type_data['damage_relations'], 99])
        
        # sort by generations with ascending order 
        dmg_relations.sort(key = lambda x : x[1])
        
        # to queue
        dmg_relations = deque(dmg_relations)

        for g in range(1, 9):
            # oldest damage relations
            dmg_rel = dmg_relations.popleft()
            
            # whether the relation is expired
            if g <= dmg_rel[1]:
                # if not, append left to reuse at the next iteration
                dmg_relations.appendleft(dmg_rel)
            else:
                # if so, get next dmg relation
                dmg_rel = dmg_relations.popleft()
                # to reuse at the next iteration
                dmg_relations.appendleft(dmg_rel)
            
            # forward relation ( effectiveness > type ) & inverse relation ( type > effectiveness )
            fwd_rel, inv_rel= get_dmg_relations(dmg_rel[0])

            # assign to the types dictionary 
            types[g][type_names['en'].lower()] = {
                'locale' : type_names,
                'fwd_rel' : fwd_rel,
                'inv_rel' : inv_rel
            }

        time.sleep(1)
    
    # delete invalid relations. 
    # steel & dark types were added at 2nd generation, and fairy at 6th generation
    # so, relation in the version before they were added is invalid
    for g, rel in types.items():
        if g < 2:
            del types[g]['steel'], types[g]['dark']
        if g < 6:
            del types[g]['fairy']
        
        # save relations by generations
        with open(f'./data/generation-{g}/relations.json', 'w') as f:
            json.dump(rel, f)


def get_pokemons(generation = 8):
    """
    Read pokemons which belong to the generation
    """
    assert 0 < generation <= 8 ,  'Invailid Generations : Corresponding generations does not exists.'
    assert type(generation) == int, 'Invailid Generations : Generations must be integer from 1 to 8.'
    return pd.read_csv(f'./data/generation-{generation}/pokemons.csv')
    

def get_generations():
    """
    Read generation-version hierarchy
    """

    with open('../data/generations.json') as f:
        return json.load(f)

def get_generation_of(version):
    """
    get generation of certain version
    """
    return [ int(g)  for g, v in get_generations().items() if version in v][0]

def fill_missing_g(flavor_texts_locale, locales):
    """
    fill missing flavor text by the most recent one
    """
    generations = get_generations()
    
    # for target locales
    for locale in locales:

        # generations which flavor text exists
        ft_existing_g = set(flavor_texts_locale[locale].keys())

        # generations which flavor text do not exist
        ft_missing_g = list(set(range(1,9)) - ft_existing_g)
        
        # to array
        feg = np.array(list(ft_existing_g))

        for missing_g in ft_missing_g:
            
            # if flavor text of the past version exists
            gs = np.where(feg < missing_g, feg, 0)
            if gs.sum() == 0:
                # if not, get the closet flavor text from the closest future version
                _g = feg[(feg- missing_g ).argmin()]
            else:
                # if so, get the flavor text from the most recent version 
                _g = gs.max()
            
            # version flavor text are copied
            copied_from = generations[str(_g)][0]

            # copy the flavor text from the version
            _ft = flavor_texts_locale[locale][_g][copied_from]

            # fill missing flavor texts 
            flavor_texts_locale[locale][missing_g] = {}
            for version in generations[str(missing_g)]:
                flavor_texts_locale[locale][missing_g][version] = [_ft, f'copied from {copied_from}, {_g}G']
    return flavor_texts_locale


def get_flavortexts(data, locales = ['en', 'ko']):
    """
    Retrieve flavor texts of the pokemon
    """

    flavor_texts = data['flavor_text_entries']
    flavor_texts_locale = { locale: {}   for locale in locales}

    for ft in flavor_texts:
        locale = ft['language']['name']
        # only target locales
        if locale in locales:
            # get generations of the flavor text
            version = ft['version']['name']
            generation = get_generation_of(version)
            
            # initialize
            if not flavor_texts_locale[locale].get(generation, False):
                flavor_texts_locale[locale][generation] = {}
            
            # asign
            flavor_texts_locale[locale][generation][version] = [ft['flavor_text'].replace('\n', ' '), 'original'] # 
    
    # fill missing generations 
    return fill_missing_g(flavor_texts_locale, locales)

def get_ability_text(ability, locales):
    """
    Retrieve flavor texts of the ability
    """

    flavor_texts_locale = { locale: {}   for locale in locales}

    for ft in ability['flavor_text_entries']:
        locale = ft['language']['name']
        # only target locales
        if locale in locales:
            # abilities differ with the "version group", not generations
            versions = VERSIONGROUP_DICT[ft['version_group']['name']]
            generation = get_generation_of(versions[0])
            
            # initialize
            if not flavor_texts_locale[locale].get(generation, False):
                flavor_texts_locale[locale][generation] = {}
            
            # get flavor texts 
            for v in versions:
                flavor_texts_locale[locale][generation][v] = [ft['flavor_text'].replace('\n', ' '), 'original'] # 

    # fill missing generations 
    return fill_missing_g(flavor_texts_locale, locales)


def get_move_text(move_inform, locales):
    """
    Retrieve flavor text of the move
    """
    flavor_texts_locale = { locale: {}   for locale in locales}

    for ft in move_inform['flavor_text_entries']:
        locale = ft['language']['name']
        # only target locale
        if locale in locales:
            # moves differ with the "version group", not generations
            versions = VERSIONGROUP_DICT[ft['version_group']['name']]
            generation = get_generation_of(versions[0])
            # initialize
            if not flavor_texts_locale[locale].get(generation, False):
                flavor_texts_locale[locale][generation] = {}
            # get flavor texts 
            for v in versions:
                flavor_texts_locale[locale][generation][v] = [ft['flavor_text'].replace('\n', ' '), 'original'] # 

    # fill missing generations 
    return fill_missing_g(flavor_texts_locale, locales)


def get_names(data, locales = ['en', 'ko']):
    """
    general functions to get names of certain attributes
    """
    names = {}
    
    for name in data['names']:
        locale = name['language']['name']
        if locale in locales:
            names[locale] = name['name']
    
    names['en'] = data['name'].lower()
    return names

def get_dmg_relations(dmg_relations):
    """
    Process damage relations of certain type with other types
    return 2 types of relations 
    - forward relations : can access to the relations by the order of relation type - effectiveness - type 
    - inverse relations : can access to the relations by the order of relation type - type - effectiveness
    """
    
    # dictionary for mapping 
    relation_dict = {
        'double_damage_from' : [2, 'defense'],
        'half_damage_from' : [0.5, 'defense'],
        'no_damage_from' : [0, 'defense'],
        'double_damage_to' : [2, 'offense'],
        'half_damage_to' : [0.5, 'offense'],
        'no_damage_to' : [0, 'offense']
    }

    # initialize 
    dmg_forward = {
        'offense' : {
            0 : [],
            0.5 : [],
            1 : [],
            2 : []
        },
        'defense'  : {
            0 : [],
            0.5 : [],
            1 : [],
            2 : []
        } }

    dmg_inversed = {
        'offense' : {},
        'defense' : {}
        }

    
    for relation, types in dmg_relations.items():
        
        ratio, relation = relation_dict[relation]
        for t in types:
            dmg_forward[relation][ratio].append(t['name'])
            dmg_inversed[relation][t['name']] = ratio

    return dmg_forward, dmg_inversed

def getRelations(generation = 8):
    """
    get relations between types by generation 
    """
    with open(f'./data/generation-{generation}/relations.json') as f:
        rel = json.load(f)

    return rel

def get_versionGroups():
    """
    get version groups 
    """
    with open('./data/versiongroups.json') as f:
        vg = json.load(f)
    return vg

def get_moves(move_inform, locales, generation):
    """
    Process moves
    """
    
    names = get_names(move_inform)
    move_dict = {}

    move_dict['name'] = names['en']
    move_dict['locale'] = names

    move_dict['power'] = move_inform['power']
    move_dict['accuracy'] = move_inform['accuracy']
    move_dict['pp'] = move_inform['pp']
    move_dict['priority'] = move_inform['priority']
    move_dict['type'] = move_inform['type']

    move_dict['flinch_chance'] = move_inform['meta'] ['flinch_chance']
    move_dict['hits'] = [move_inform['meta']['min_hits'], move_inform['meta']['max_hits']] if move_inform['meta']['max_hits'] or move_inform['meta']['min_hits'] else [1,1]
    move_dict['damage_class'] = move_inform['damage_class']['name']
    flavor_texts = get_move_text(move_inform, locales)
    move_dict['flavor_text'] = [ flavor_texts[locale][generation] for locale in flavor_texts.keys()] # get_move_text(move_inform, locales)[generation]

    return move_dict



VERSIONGROUP_DICT = get_versionGroups()

# 기술을 세대별로 저장 (위력이나 뭐 그런게 바뀜)

moves_8 = pd.read_csv('../data/generation-8/moves.csv')

for url in moves_8['url'].values.tolist():
    move = get_inform(url)
    if len(move['past_values']) >= 2:
        break
    time.sleep(0.5)


move['past_values']

get_names(move)

move['past_values'][0]

# version group으로 가서
# 그 group의 세대를 조회하고
# 다음 세대가 나올 때 까지
# 해당 정보를 사용

from copy import deepcopy


moves = { generation : {} for generation in range(1, 9)}

generation = 1
move = get_inform(moves_8['url'][1])

latest_move = get_moves(move, locales = ['en', 'ko'])

past_moves = move['past_values']

past_move = past_moves[0]

_past_g = get_generation_of(VERSIONGROUP_DICT[past_move['version_group']['name']][0])

past_keys = set(past_move.keys())


_g_move = deepcopy(move)

for key in past_keys:
    _g_move[key] = past_move[key]

moves[generation] = _g_move
get_moves(_g_move, ['en', 'ko'], 6)




    
for i in range(1, 19):

    # type data
    type_data = get_inform(f'https://pokeapi.co/api/v2/type/{i}')
    
    # type names
    type_names = get_names(type_data)

    # damage relation & generation pairs
    dmg_relations = [ [dmg_rel['damage_relations'], GENERATION_DICT[dmg_rel['generation']['name']]] for dmg_rel in  type_data['past_damage_relations']]
    dmg_relations.append([type_data['damage_relations'], 99])
    
    # sort by generations with ascending order 
    dmg_relations.sort(key = lambda x : x[1])
    
    # to queue
    dmg_relations = deque(dmg_relations)

    for g in range(1, 9):
        # oldest damage relations
        dmg_rel = dmg_relations.popleft()
        
        # whether the relation is expired
        if g <= dmg_rel[1]:
            # if not, append left to reuse at the next iteration
            dmg_relations.appendleft(dmg_rel)
        else:
            # if so, get next dmg relation
            dmg_rel = dmg_relations.popleft()
            # to reuse at the next iteration
            dmg_relations.appendleft(dmg_rel)
        
        # forward relation ( effectiveness > type ) & inverse relation ( type > effectiveness )
        fwd_rel, inv_rel= get_dmg_relations(dmg_rel[0])

        # assign to the types dictionary 
        types[g][type_names['en'].lower()] = {
            'locale' : type_names,
            'fwd_rel' : fwd_rel,
            'inv_rel' : inv_rel
        }

    time.sleep(1)

# delete invalid relations. 
# steel & dark types were added at 2nd generation, and fairy at 6th generation
# so, relation in the version before they were added is invalid
for g, rel in types.items():
    if g < 2:
        del types[g]['steel'], types[g]['dark']
    if g < 6:
        del types[g]['fairy']
    
    # save relations by generations
    with open(f'./data/generation-{g}/relations.json', 'w') as f:
        json.dump(rel, f)



move.keys()

# generation = 1
# pokemon_index = 1
# locale = 'ko'

# # pokemons in specific generations
# pokemons = get_pokemons(generation)

# # data of the pokemon
# data = get_inform(pokemons['url'][pokemon_index])

# # the generation the pokemon first appeared
# generationAppeared = pokemons['generations'][pokemon_index]

# data['evolution_chain'] # self-chain 걸어서 from / to 하면 됨

# # 전포인지 아닌지

# data.keys()

# data['shape']


# # get simple description
# get_flavortexts(data, locales)[locale][generation]

# # name
# get_names(data, locales)[locale]

# # specifications
# specifications = get_inform(pokemons['url'][pokemon_index].replace('-species', ''))

# type_names = [ rel[t['type']['name']]['locale'][locale]  for t in specifications['types']]

# # type relataion json
# rel = getRelations(generation)

# # abilities
# abilities = specifications['abilities']

# ability =  get_inform(abilities[0]['ability']['url'])
# get_ability_text(ability, locales)[locale][generation]


# move = specifications['moves'][1]

# move['move']
# move['version_group_details'][15]


# move_inform = get_inform(move['move']['url'])
# get_moves(move_inform, locales)

# move_inform['flavor_text_entries']

# stats = { stat['stat']['name'] : stat['base_stat']  for stat in specifications['stats']}
# stats['total'] = sum(stats.values())

# 세대별로 다 다름
# 당연~히 세대별로 따로 만들어야 한다. 
# 귀찮아 지는데

# 난 이거 django 써야됨.. 
# django + vue (비동기 날먹하려고)
# 비슷한 차트를 공유하니까.. 

# 그러면

# 1. 세대별 포켓몬 종류 다 알아야 하고
# 2. 세대별 포켓몬 별 특성 / 타입 / 전포환포 여부 다 넣고
# 3. 세대별 포켓몬 별 기술 / 특징 다 알아야 함. (교배로 배우는지 뭘로 배우는 지 등)

# 글면 필요한 모델이?

# generations
# versions
# locale ?

# Pokemon
# - pokedex_index : IntegerField
# - gernations : ForiegnKey(PokeGeneration)
# - name : CharField
# - is_mythical : BooleanField
# - is_legendary : BooleanField
# - flavor_text : TextField
# - abilities : ManytoManyField(PokeAbility)
# - moves : ManytoManyFields(PokeMove)
# - types : ManytoManyFields(PokeType)
# - locale : ForiegnKey(Locale)
# - **stats : IntegerField

# PokeGeneration
# - name

# PokeVersion
# - generation : ForiegnKey(PokeGeneration)
# - name : CharField
# - locale : ForiegnKey(Locale)

# PokeAbility
# - generation : ForiegnKey(PokeGeneration)
# - description : TextField
# - locale : ForiegnKey(Locale)

# PokeMove
# - Generation : ForiegnKey(PokeGeneration)
# - name : CharField
# - locale : ForiegnKey(Locale)
# - power : IntegerField
# - accuracy : IntegerField
# - pp : IntegerField
# - priority : BooleanField
# - type : ManytoManyField(Type)
# - flinch_chance : IntegerField
# - hits : PickleobjField
# - damage_class : CharField
# - flavor_text : TextField

# PokeType
# - name : CharField
# - generation : ForiegnKey(PokeGeneration)
# - color : TextField

# Locale 
# - name



#get_moves(move_inform, locales).keys()