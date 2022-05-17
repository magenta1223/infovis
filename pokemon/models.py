from django.db import models

# Create your models here.


class Locale(models.Model):
    language = models.CharField(max_length= 2, unique= True)
    def __str__(self):
        return self.language

class Ability(models.Model):
    ability_index = models.IntegerField()
    name = models.TextField()
    description = models.TextField()
    locale = models.ForeignKey(Locale, on_delete= models.CASCADE)    


    

class PokeType(models.Model):
    type_index = models.IntegerField()
    name = models.CharField(max_length = 10)
    color = models.CharField(max_length= 7)
    locale = models.ForeignKey(Locale, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.name
        
class Move(models.Model):
    move_index = models.IntegerField()
    name = models.CharField(max_length= 40)
    locale = models.ForeignKey(Locale, on_delete= models.CASCADE)    
    power = models.IntegerField(default= 0)
    hit_prob = models.IntegerField(default=0)
    pp = models.IntegerField(default = 0)
    priority = models.IntegerField(default = False)
    flinch_rate = models.IntegerField(default = 0)
    min_hits = models.IntegerField(default = 1)
    max_hits = models.IntegerField(default = 1)
    damage_cls = models.CharField(max_length= 20)
    flavor_text = models.TextField()
    type = models.ForeignKey(PokeType, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

class Pokemon(models.Model):
    pokedex_index = models.IntegerField(verbose_name='도감번호', default = -1)
    name = models.CharField(max_length= 50)
    is_mythical = models.BooleanField(default= False)
    is_legendary= models.BooleanField(default= False)
    description = models.TextField(default = "")
    locale = models.ForeignKey(Locale, on_delete= models.CASCADE)
    hp = models.IntegerField(verbose_name= '체력', default = 0)
    attack = models.IntegerField(verbose_name= '공격', default = 0)
    defense = models.IntegerField(verbose_name= '방어', default = 0)
    spattack = models.IntegerField(verbose_name= '특수공격', default = 0)
    spdefense = models.IntegerField(verbose_name= '특수방어', default = 0)
    speed = models.IntegerField(verbose_name= '스피드', default = 0)
    total = models.IntegerField(verbose_name= '총합', default = 0)

    abilities = models.ManyToManyField(Ability, related_name= 'abilities')
    types = models.ManyToManyField(PokeType, related_name= 'types')
    
    evolves_from = models.IntegerField(blank= True, null = True)
    evolves_to = models.IntegerField(blank= True, null = True)

    isBaby = models.BooleanField(default= False)
    
class PokeMove(models.Model):
    # pokemon과 move가 many-to-many긴 한데
    # 거기에 부가적인 정보 (learning way, level 등)이 다 달라서 따로 만들어 줘야 함
    # 아마 대충 50~100K row
    pokemon = models.ForeignKey(Pokemon, on_delete= models.CASCADE, related_name= 'pokemove')
    move = models.ForeignKey(Move, on_delete= models.CASCADE)
    learning_way = models.CharField(max_length= 20)
    learning_level = models.IntegerField(default = 0)

