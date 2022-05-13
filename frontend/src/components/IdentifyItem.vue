<template>
    <v-container>
        <v-row>
            <v-col cols="6">
                <v-card :loading="true">
                    <v-row>
                        <v-img :src="imgSrc"/>    
                    </v-row>

                    <v-row>
                        <v-col cols="6">
                            <v-card-title>{{item.name}}</v-card-title>
                        </v-col>
                        <v-col v-for="type in item.types" :key="type.id" cols="3" class="mt-3">
                            <v-btn :color="type.color" class="align-self-center" small>{{type.name}}</v-btn>
                        </v-col>
                    </v-row>
                    



                    <v-card-text class="text-start">
                            {{item.description}}
                    </v-card-text>
                    <v-divider class="mx-4"></v-divider>
                    <v-card-title>Abilities</v-card-title>



                    <v-card-text v-for="ability in item.abilities" :key="ability.id" class="text-start">
                        <div style="color:black">
                            {{ability.name}}
                        </div>
                        <div>
                            {{ability.description}}
                        </div>
                    </v-card-text>
                    
                    

                    <v-row>
                        <v-col>
                            <v-row v-for="move in item.pokemove" :key="move.id">
                                이름 : {{move.move.name}}
                                위력 : {{move.move.power}}
                                명중률 : {{move.move.hit_prob}}
                                설명 : {{move.move.flavor_text}}
                                <!-- name power hit_prob flavor text -->
                            </v-row>
                        </v-col>
                    </v-row>
                </v-card>

            </v-col>
            <v-col cols="6">
                <svg id="radar"></svg>
            </v-col>
        </v-row>
    </v-container>


</template>


<script>
import RadarChart from '../d3Chart/radar.js'
//import axios from 'axios'

let spriteUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'

export default {
    data() {
        return {
            items : [],
            radarchart : "#radar",
            features : {
                "en" : [['HP', 0], ['ATTACK', 1],[ 'DEFENSE', 2], ['SP.ATTACK', 3], ['SP.DEFENSE', 4], ['SPEED', 5]],
                "ko" : [['체력', 0], ['공격', 1], ['방어', 2], ['특수공격', 3], ['특수방어', 4], ['스피드', 5]]  
            },
        }
    },

    components : {
        
    },


    props : ['item', 'locale'],

    methods : {

 

    },
        
    mounted() {
        console.log(this.item)

        console.log(this.features[this.locale])
        this.radarchart = new RadarChart(this.radarchart, this.features[this.locale], 300, 300)
        this.radarchart.initialize()
        this.radarchart.update(this.item, "retrieve")

        //axios({
        //    method: "GET",
        //    url : `${spriteUrl}${this.item.pokedex_index}.png`
        //}).then( (response) => {
        //    console.log(response.data[0].url)
         //   this.imgSrc = response.data[0].url
        //}).catch((response) => {
        //    console.log(response.data)
        //})


    },

    watch : {
        item : function(){
            this.radarchart.update(this.item, "retrieve")
        }
    },

    computed : {
        imgSrc : function() {
            return `${spriteUrl}${this.item.pokedex_index}.png`
        }
    }
}
</script>


<style>
    body {
        font-family: 'Open Sans', sans-serif;
        font-size: 11px;
        font-weight: 300;
        fill: #242424;
        text-align: center;
        text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff, 0 -1px 0 #fff;
        cursor: default;
    }

    .legend {
        font-family: 'Raleway', sans-serif;
        fill: #333333;
    }

    .tooltip {
        fill: #333333;
    }
</style>


