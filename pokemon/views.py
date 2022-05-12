from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .serailizers import PokeTypeSerializer, PokemonRetrieveSerializer, PokemonSerializer
from .models import * 
from rest_framework import viewsets # vieset import

from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics 
import json

from django.db.models import Q

from .models import *

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
        return Response(serializer.data)

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
