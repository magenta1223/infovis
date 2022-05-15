from .views import *
from django.urls import include, path
from rest_framework import routers, urls  # router import


router = routers.DefaultRouter()  # DefaultRouter 설정
router.register('pokemon', PokemonViewSet) 
router.register('poketype', PokeTypeViewSet) 


urlpatterns = [
    path('', include(router.urls)),
    path('counter/', CounterView.as_view(), name=  'counter')
]