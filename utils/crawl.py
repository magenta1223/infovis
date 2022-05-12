from utils.crawl_funcs import *
from pokemon.models import *
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q





def localesDB():
    Locale.objects.all().delete()
    for locale in ['en', 'ko']:
        _instance = Locale(language = locale)
        _instance.save()

def typesToDB():
    PokeType.objects.all().delete()
    typeColorPair = getTypes()
    locales = Locale.objects.all()
    locales = {locale : locales.filter(Q(language__iexact = locale))[0] for locale in ['en', 'ko']}
    for key, val in typeColorPair.items():
        for locale in ['en', 'ko']:
            _type = PokeType(type_index = val[1] , name = val[2][locale] , color = val[0], locale = locales[locale] )
            _type.save()

localesDB()

def movesToDB():
    Move.objects.all().delete()
    moves = pd.read_csv('./data/moves.csv')
    LOCALES = Locale.objects.all()
    for url in moves['url']:
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
        time.sleep(0.5)

def abilitiesToDB():
    Ability.objects.all().delete()
    abilities = getAbilities()
    LOCALES = Locale.objects.all()
    for url in abilities['url']:
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
                print(names, url)
        time.sleep(0.5)



def pokemonsToDB():
    Pokemon.objects.all().delete()
    PokeMove.objects.all().delete()
    pokemons = getPokemons()
    LOCALES = Locale.objects.all()
    ALL_ABILITIES = Ability.objects.all()
    ALL_TYPES = PokeType.objects.all()
    ALL_MOVES = Move.objects.all()
    for url in pokemons['url']:
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
        time.sleep(0.5)





def main():
    crwalPokemons()
    crawlTypes()
    crawlAbilities()

    generateModels(Locale)
    generateModels(PokeType)

    locales = Locale.objects.all()
    LOCALES = {locale : locales.filter(Q(language__iexact = locale))[0] for locale in ['en', 'ko']}

    movesToDB()
    abilitiesToDB()
    pokemonsToDB()

