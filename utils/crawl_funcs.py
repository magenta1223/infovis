from asyncio.windows_events import NULL
from distutils.log import WARN
import requests
import json
import pandas as pd
import time
import os
import pickle
import numpy as np
from collections import deque
from pokemon.models import *
from django.db.models import Q
from tqdm import tqdm

locales = ['en', 'ko']

# for stable crawling 
# takes 40 minutes
SLEEP = 0.2


def getInform(url):
    """
    get information as json from api endpoint (url) 
    """
    return json.loads(requests.get(url).content)

def getID(url):
    return int(url.split('/')[-2])


def null_parser(value):
    if value == None:
        return 0
    else:
        return value


def crwalPokemons():
    """
    Crawl key attributes of pokemons by generations
    """
    
    
    # make dirs
    if not os.path.exists(f'./data'):
        print('Generating directory for the data..')
        os.makedirs('./data')
    
    # initialize
    poke_df = []
    move_df = []

    print('Start crawl pokemons..')

    for generation in range(1, 9):
        # get pokemons added newly at the generation 
        pokemons = getInform(f'https://pokeapi.co/api/v2/generation/{generation}/')

        # preprocess
        ## pokemons
        _poke_df = pd.DataFrame(pokemons['pokemon_species'])
        _poke_df['pokedex_index'] = _poke_df['url'].apply(getID)
        _poke_df = _poke_df.sort_values('pokedex_index').reset_index(drop = True)
        ## moves
        _move_df = pd.DataFrame(pokemons['moves'])
        _move_df['move_index'] = _move_df['url'].apply(getID)
        _move_df = _move_df.sort_values('move_index').reset_index(drop = True)

        # acummulate
        poke_df.append(_poke_df)
        move_df.append(_move_df)
        
        # for stable crawling
        time.sleep(SLEEP)

    # save the pokemons accumulated upto this generation  as csv 
    pd.concat(poke_df, axis = 0).to_csv(f'./data/pokemons.csv', index = False)
    pd.concat(move_df, axis = 0).to_csv(f'./data/moves.csv', index = False)
    print('Done ! \nYou can see the results in ./data')





def crawlTypes():
    """
    Crawl All Types
    """
    
    print('Generating relations..')

    # initialize
    types = {}

    for i in range(1, 19):

        # type data
        type_data = getInform(f'https://pokeapi.co/api/v2/type/{i}')
        
        # type names
        type_names = getNames(type_data)

        # damage relation & generation pairs
        dmg_relations = type_data['damage_relations']

        fwd_rel, inv_rel= parseDmgRelations(dmg_relations)

        types[type_names['en'].lower()] = {
                'locale' : type_names,
                'fwd_rel' : fwd_rel,
                'inv_rel' : inv_rel
            }
    
        time.sleep(SLEEP)
 
    # save relations by generations
    with open(f'./data/relations.json', 'w') as f:
        json.dump(types, f)
    print('Done!')


def crawlAbilities():
    print('Start crawl abilities..')
    url = "https://pokeapi.co/api/v2/ability/?offset=0&limit=400"  
    abilities = getInform(url)['results']
    pd.DataFrame(abilities).to_csv('./data/abilities.csv', index = False)
    print('Done!')

def getPokemons():
    """
    Read pokemons
    """
    return pd.read_csv(f'./data/pokemons.csv')

def getAbilities():
    """
    Read all abilities
    """
    return pd.read_csv(f'./data/abilities.csv')


def getTypes():
    try :
        with open(f'./data/typecolors.json', encoding = 'utf-8') as f:
            typeColorPair = json.load(f)
    except:
        with open(f'C:/HW/infovis/final/config/data/typecolors.json', encoding = 'utf-8') as f:
            typeColorPair = json.load(f)       

    return typeColorPair


def getText(inform, locales):
    flavor_texts_locale = { locale: ''  for locale in locales}

    for ft in inform['flavor_text_entries']:
        locale = ft['language']['name']
        # only target locale
        if locale in locales:
            flavor_texts_locale[locale] = ft['flavor_text'].replace('\n', ' ') if ft['flavor_text'] else ''

    return flavor_texts_locale


def getNames(data, locales = ['en', 'ko']):
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

def parseDmgRelations(dmg_relations):
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

def getRelations():
    """
    get relations between types by generation 
    """
    with open(f'./data/relations.json') as f:
        rel = json.load(f)
    return rel

def parseMove(move_inform, locales):
    """
    Process moves
    """
    
    names = getNames(move_inform)
    move_dict = {}
    move_dict['id'] = move_inform['id']

    move_dict['name'] = names['en']
    move_dict['locale'] = names

    move_dict['power'] = null_parser(move_inform['power'])
    move_dict['accuracy'] = null_parser(move_inform['accuracy'])
    move_dict['pp'] = null_parser(move_inform['pp'])
    move_dict['priority'] = null_parser(move_inform['priority'])
    move_dict['type'] = null_parser(move_inform['type'])

    if move_inform['meta'] == None:
        move_dict['flinch_chance'] = 0
        move_dict['min_hits'] = 1
        move_dict['max_hits'] = 1
    else :
        move_dict['flinch_chance'] = null_parser(move_inform['meta'] ['flinch_chance'])
        move_dict['min_hits'] = null_parser(move_inform['meta']['min_hits']) if move_inform['meta']['min_hits'] else 1 
        move_dict['max_hits'] = null_parser(move_inform['meta']['max_hits']) if move_inform['meta']['min_hits'] else 1 

    move_dict['damage_class'] = null_parser(move_inform['damage_class']['name'])
    move_dict['flavor_text'] = getText(move_inform, locales)

    return move_dict

def parsePokemon(pokemon_url, locales):
    
    poke_dict = {}

    # pokemon
    pokemon = getInform(pokemon_url)
    spec = getInform(pokemon_url.replace('-species', ''))

    types = getTypes()

    poke_dict['index'] = pokemon['id']
    poke_dict['names'] = getNames(pokemon, locales)
    poke_dict['is_mythical'] = pokemon['is_mythical']
    poke_dict['is_legendary'] = pokemon['is_legendary']
    poke_dict['description'] = getText(pokemon, locales)
    poke_dict['types'] = [ types[t['type']['name']][1]  for t in spec['types']]
    poke_dict['stats'] = { stat['stat']['name'] : stat['base_stat']  for stat in spec['stats']} 
    poke_dict['abilities'] = [ getID(a['ability']['url'])  for a in spec['abilities']]
    poke_dict['evolves_from'] = getID(pokemon['evolves_from_species']['url']) if pokemon['evolves_from_species'] else 0
    
    # mvoes    
    poke_dict['moves'] = {}
    for move in spec['moves']:
        move_id = getID(move['move']['url'])
        learnings = { (v['move_learn_method']['name'], v['level_learned_at']) for v in move['version_group_details'] }
        poke_dict['moves'][move_id] = learnings

    return poke_dict
    
        
def localesDB():
    print('Generating locales (English, Korean) ..\nTo customize, Edit localesDB in ./utils/crawl_funcs.py')
    Locale.objects.all().delete()
    for locale in ['en', 'ko']:
        _instance = Locale(language = locale)
        _instance.save()
    print('Done!')

def typesToDB():
    print('Generating pokemon`s types..')
    PokeType.objects.all().delete()
    typeColorPair = getTypes()
    LOCALES = {locale : Locale.objects.all().filter(Q(language__iexact = locale))[0] for locale in ['en', 'ko']}
    for key, val in tqdm(typeColorPair.items()):
        for locale in ['en', 'ko']:
            _type = PokeType(type_index = val[1] , name = val[2][locale] , color = val[0], locale = LOCALES[locale] )
            _type.save()
    print('Done!')


def movesToDB():
    print('Start crawling all the moves..')
    Move.objects.all().delete()
    moves = pd.read_csv('./data/moves.csv')
    LOCALES = {locale : Locale.objects.all().filter(Q(language__iexact = locale))[0] for locale in ['en', 'ko']}
    for url in tqdm(moves['url']):
        if int(url.split('/')[-2]) > 10000:
            continue
        move_inform = getInform(url)
        move = parseMove(move_inform, ['en', 'ko'])
        for locale in ['en', 'ko']:
            instance = Move(
                move_index = move['id'],
                name = move['locale'][locale],
                locale = LOCALES[locale],
                power = move['power'],
                hit_prob = move['accuracy'],
                pp = move['pp'],
                priority = move['priority'],
                flinch_rate = move['flinch_chance'],
                min_hits = move['min_hits'],
                max_hits = move['max_hits'],
                damage_cls = move['damage_class'],
                flavor_text = move['flavor_text'][locale],
            )
            instance.save()
        time.sleep(SLEEP)
    print('Done!')

def abilitiesToDB():
    print('Start crawling all the abilities..')
    Ability.objects.all().delete()
    abilities = getAbilities()
    LOCALES = {locale : Locale.objects.all().filter(Q(language__iexact = locale))[0] for locale in ['en', 'ko']}
    for url in tqdm(abilities['url']):
        ability = getInform(url)
        ability_text = getText(ability, ['en', 'ko'])
        names = getNames(ability)
        for locale in ['en', 'ko']:
            try:
                instance = Ability(
                    ability_index = ability['id'],
                    name = names[locale],
                    locale = LOCALES[locale],
                    description = ability_text[locale])
                instance.save()
            except:
                pass
        time.sleep(SLEEP)
    print('Done!')



def pokemonsToDB():
    print('Start crawling all the pokemons..')
    Pokemon.objects.all().delete()
    PokeMove.objects.all().delete()
    pokemons = getPokemons()
    LOCALES = {locale : Locale.objects.all().filter(Q(language__iexact = locale))[0] for locale in ['en', 'ko']}
    ALL_ABILITIES = Ability.objects.all()
    ALL_TYPES = PokeType.objects.all()
    ALL_MOVES = Move.objects.all()
    for url in tqdm(pokemons['url']):
        pokemon = parsePokemon(url, ['en', 'ko'])
        for locale in ['en', 'ko']:
            instance = Pokemon(
                pokedex_index = pokemon['index'],
                name = pokemon['names'][locale],
                is_mythical = pokemon['is_mythical'],
                is_legendary = pokemon['is_legendary'],
                description = pokemon['description'][locale],
                hp = pokemon['stats']['hp'],
                attack = pokemon['stats']['attack'],
                defense = pokemon['stats']['defense'],
                spattack = pokemon['stats']['special-attack'],
                spdefense = pokemon['stats']['special-defense'],
                speed = pokemon['stats']['speed'],
                total = sum(pokemon['stats'].values()),
                evolves_from = pokemon['evolves_from'],
                locale = LOCALES[locale]
            )
            instance.save()
            # add abilities
            abilities = ALL_ABILITIES.filter(Q(ability_index__in = pokemon['abilities']) & Q(locale__language__iexact = locale))
            instance.abilities.add(*abilities) 
            # add types
            types = ALL_TYPES.filter(Q(type_index__in = pokemon['types']) & Q(locale__language__iexact = locale))
            instance.types.add(*types)
            instance.save()
            for id, learnings in pokemon['moves'].items():
                move = ALL_MOVES.filter(Q(move_index = id) & Q(locale__language__iexact = locale))[0]
                for learning in learnings:
                    pokemove = PokeMove(
                        pokemon = instance,
                        move = move,
                        learning_way = learning[0],
                        learning_level = learning[1]
                    )
                    pokemove.save()
        time.sleep(SLEEP)
    print('Done!')