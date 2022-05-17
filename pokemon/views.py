from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics # vieset import
from rest_framework.response import Response
from rest_framework import generics 
from django.db.models import Q

from .serializers import PokeTypeSerializer, PokemonRetrieveSerializer, PokemonSerializer
from .models import * 
from .models import *
from utils.counter import * 


def parsePokemove(pokemove):
    return {'move' : pokemove['move'], 'learningWay' : [pokemove['learning_way']]}

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def list(self, request, pk=None):
        kwargs = request.query_params

        pokemons_locale = self.queryset.filter(
            Q(locale__language__iexact = kwargs['locale'])
        )
        serializer = PokemonSerializer(data=pokemons_locale, many = True)
        serializer.is_valid()
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pokemon = get_object_or_404(self.queryset, pk=pk)
        serializer = PokemonRetrieveSerializer(pokemon)

        moves = serializer.data['pokemove']
        filteredMoves = []
        keys = []
        
        for move in moves:
            if move['move']['id'] not in keys:
                keys.append(move['move']['id'])
                filteredMoves.append(parsePokemove(move))
            elif filteredMoves[keys.index(move['move']['id'])]['learningWay'] == move['learning_way']:
                continue
            else:
                filteredMoves[keys.index(move['move']['id'])]['learningWay'].append(move['learning_way'])

        return Response({"data" : serializer.data, "moves" : filteredMoves})

class PokeTypeViewSet(viewsets.ModelViewSet):
    queryset = PokeType.objects.all()
    serializer_class = PokeTypeSerializer

    def list(self, request, pk=None):
        kwargs = request.query_params

        pokemons_locale = self.queryset.filter(
            Q(locale__language__iexact = kwargs['locale'])
        )
        serializer = self.get_serializer(data=pokemons_locale, many = True)
        serializer.is_valid()

        return Response(serializer.data)


class CounterView(generics.GenericAPIView):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

    def get(self, request, *args, **kwargs):


        kwargs = request.query_params

        print('counter', kwargs)

        actor = self.get_serializer(self.queryset.filter(
            Q(locale__language__iexact = kwargs['locale']) &
            Q(pokedex_index = kwargs['pokedex_index'])
        )[0]).data

        # actor = PokemonSerializer(queryset.filter(
        #     Q(locale__language__iexact = 'en') &
        #     Q(pokedex_index = 1)
        # )[0]).data


        targets = self.get_serializer(
            data = self.queryset.filter(
                Q(locale__language__iexact = kwargs['locale']) &
                Q(isBaby = False)
            ),
            many = True
            )




        targets.is_valid()
        
        counters = []
        for target in targets.data:
            print(target['name'])
            counter, index = battleSimulation(actor, target)
            if counter:
                print(target['name'])
                counters.append(target['pokedex_index'])
        
        counterset = self.queryset.filter(
            Q(locale__language__iexact = kwargs['locale']) &
            Q(pokedex_index__in = counters)
        )

        serializer =  self.get_serializer(data = counterset, many = True)
        serializer.is_valid()
    
        return Response(serializer.data)