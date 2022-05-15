<template>
    <div style="width:100%">
        <v-card :loading="true">
            <!-- sprite & stats -->
            <v-row>
                <v-col cols = "6">
                    <v-img :src="imgSrc"/> 
                </v-col>
                <v-col cols = "6">
                    <svg id="radar"></svg>
                </v-col>
            </v-row>

            <!-- name & types -->
            <v-row>
                <v-card-title class="ma-3">{{item.data.name}}</v-card-title>
                <v-btn v-for="type in item.data.types" :key="type.id" :color="type.color" class="align-self-center ma-1" small>{{type.name}}</v-btn>
            </v-row>

            <!-- description -->
            <v-card-text class="text-start">
                    {{item.data.description}}
            </v-card-text>
            <v-divider class="mx-4"></v-divider>
            <!-- Abilities -->
            <v-card-title>Abilities</v-card-title>
            <v-card-text v-for="ability in item.data.abilities" :key="ability.id" class="text-start">
                <div style="color:black">
                    {{ability.name}}
                </div>
                <div>
                    {{ability.description}}
                </div>
            </v-card-text>
            
            <!-- Available moves -->
            <v-card-title>Moves</v-card-title>
                <v-select
                v-model="selectedTypes"
                class="mb-4 ml-4 mr-4"
                item-text="name"
                item-value="type_index"
                :items="types"
                attach
                chips
                label="Types"
                :menu-props="{ top: false, offsetY: true }"
                @change="filter()"
                >
                    <template #selection="{ item }">
                        <v-chip :color="item.color">{{item.name}}</v-chip>
                    </template>
                </v-select>

            <!-- <v-row class="ma-4">
                <StatSlider :stat="'POWER'" :task="task" :vertical="false" @input="setVal"/>
            </v-row> -->
            <v-row>
                <v-col>
                    <v-data-table
                        :headers="headers[locale]"
                        :items="filteredMoves"
                        multi-sort
                        class="elevation-1"
                    >
                    <template v-slot:[`item.type`]="{ item }">
                        <v-btn :color="item.type.color" small> {{item.type.name}}</v-btn>
                    </template>
                    </v-data-table>
                </v-col>
            </v-row>
        </v-card>
        <v-btn @click="counter()">find counter</v-btn>
        
    </div>


</template>


<script>
import RadarChart from '../d3Chart/radar.js'
// import StatSlider from './StatSlider.vue'
import axios from 'axios'

//import axios from 'axios'

let spriteUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'

export default {
    data() {
        return {
            features : {
                "en" : [['HP', 0], ['ATTACK', 1],[ 'DEFENSE', 2], ['SP.ATTACK', 3], ['SP.DEFENSE', 4], ['SPEED', 5]],
                "ko" : [['체력', 0], ['공격', 1], ['방어', 2], ['특수공격', 3], ['특수방어', 4], ['스피드', 5]]  
            },
            headers : {
                "en" : [
                    {text : 'Name', value : 'name'},
                    {text : 'Power', value : 'power'},
                    {text : 'PP', value : 'pp'},
                    {text : 'Description', value : 'flavor_text'},
                    {text : 'Type', value : 'type'},
                ],
                "ko" : [
                    {text : '이름', value : 'name'},
                    {text : '위력', value : 'power'}, 
                    {text : 'PP', value : 'pp'}, 
                    {text : '설명', value : 'flavor_text'},
                    {text : '타입', value : 'type'}
                ]
            },
            moves : [],
            selectedTypes : [],
            types : [],
            filtered : [],
            filteredMoves : []
        }
    },

    components : {
        // StatSlider
    },

    props : ['item', 'locale'],

    methods : {
        counter : function(){
            this.$emit('counter', true)
        },
        fetchTypes : function() {
            axios({
                method : "GET",
                url : 'http://127.0.0.1:8000/api/poketype/',
                params : {
                    locale : this.locale
                }
            }).then( (response) => {
                this.types = response.data
            }).catch((response) => {
                console.log('Failed', response)
            })
        },
        filter : function(){
            let filtered = this.moves.filter((d) => (d.type.type_index === this.selectedTypes))
            if (filtered.length > 0){
                this.filteredMoves = filtered
            } else {
                alert('no items')
                this.selectedTypes = []
                this.filteredMoves = this.moves
            }
        }
    },
        
    mounted() {
        console.log(this.item)
        console.log(this.features[this.locale])
        this.fetchTypes()
        this.radarchart = new RadarChart("#radar", this.features[this.locale], 300, 300)
        this.radarchart.initialize()
        this.radarchart.update(this.item, "retrieve")
    },

    watch : {
        item : function(){
            this.radarchart.update(this.item.data, "retrieve")
            this.moves = this.item.moves.map( (d) => (d.move) )
            this.filteredMoves = this.moves
        }
    },

    computed : {
        imgSrc : function() {
            return `${spriteUrl}${this.item.data.pokedex_index}.png`
        },
    }
}
</script>

