from utils.crawl_funcs import *
from pokemon.models import *
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crawl data'

    def handle(self, *args, **kwargs):
        crwalPokemons()
        crawlTypes()
        crawlAbilities()
        localesDB()
        typesToDB()
        movesToDB()
        abilitiesToDB()
        pokemonsToDB()