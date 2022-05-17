# evolves_from에 내 pokedex_index를 가지는 녀석이 있으면? baby임
# 아무도 없으면? baby아님 ㅎ

from pokemon.models import Pokemon
from django.db.models import Q

def baby():

    enPokemons = Pokemon.objects.all().filter(
        Q(locale__language__iexact = "en")
    )

    allIndices = set(range(1, 899))

    babies = set()

    for pokemon in enPokemons:
        babies.add(pokemon.evolves_from)

    notBabies = allIndices - babies
    babies = Pokemon.objects.all().filter(pokedex_index__in = babies)
    notBabies = Pokemon.objects.all().filter(pokedex_index__in = notBabies)

    for baby in babies:
        baby.isBaby = True
        baby.save()

    for adult in notBabies:
        adult.isBaby = False
        adult.save()


    
    
        