from rest_framework import serializers # serializer import
from .models import * # 선언한 모델 import

class LocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locale
        fields = '__all__'

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'

class PokeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PokeType
        fields = '__all__'


class PokeMoveSerializer(serializers.ModelSerializer):
    move = MoveSerializer()
    class Meta:
        model = PokeMove
        fields = '__all__'

class PokemonRetrieveSerializer(serializers.ModelSerializer):
    pokemove = PokeMoveSerializer(many = True)
    types = PokeTypeSerializer(many = True)
    abilities = AbilitySerializer(many = True)
    
    class Meta:
        model = Pokemon
        fields = '__all__'


class PokemonSerializer(serializers.ModelSerializer):
    types = PokeTypeSerializer(many = True)
    class Meta:
        model = Pokemon
        fields = '__all__'


