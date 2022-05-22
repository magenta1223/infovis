<template>
    <div style="width:100%">
        <v-card
        height="900"
        class="overflow-y-auto overflow-x-hidden">
            <!-- sprite & stats -->
            <v-row>
                <v-col cols = "5">
                    <v-img :src="imgSrc" max-width="400"  /> 
                </v-col>
                <v-col cols = "7">
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
            <v-card-title>{{ locale == "en" ? "Abilities" : "특성"}}</v-card-title>
            <v-card-text v-for="ability in item.data.abilities" :key="ability.id" class="text-start">
                <div style="color:black">
                    {{ability.name}}
                </div>
                <div>
                    {{ability.description}}
                </div>
            </v-card-text>
            
            <!-- Available moves -->
            <v-card-title>{{ locale == "en" ? "Moves" : "기술"}}</v-card-title>
                <TypeFilter
                :locale="locale"
                :csshelper="'mb-4 ml-4 mr-4'"
                :multiple="false"
                @filter="filter"
                />
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
    </div>


</template>


<script>
import RadarChart from '../d3Chart/radar.js'
import TypeFilter from "./TypeFilter.vue"

//import axios from 'axios'

let spriteUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'

export default {
    // template variables 
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
                    {text : 'Description', value : 'flavor_text'},
                    {text : 'Type', value : 'type'},
                ],
                "ko" : [
                    {text : '이름', value : 'name'},
                    {text : '위력', value : 'power'}, 
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
        TypeFilter
    },


    // template variables from upper parent component
    props : ['item', 'locale'],
    
    // js function 
    methods : {
        filter : function(selectedTypes){
            // filter moves by selected types
            let filtered = this.moves.filter((d) => (d.type.type_index === selectedTypes))
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
        // run right after the page mounted 
        this.radarchart = new RadarChart("#radar", this.features[this.locale], 200, 250)
        this.radarchart.initialize()
        this.radarchart.update(this.item)
    },

    watch : {
        // works as the eventlistener
        item : function(){
            this.radarchart.update(this.item.data)
            this.moves = this.item.moves.map( (d) => (d.move) )
            this.filteredMoves = this.moves
        }
    },

    computed : {
        // dynamic variable
        imgSrc : function() {
            return `${spriteUrl}${this.item.data.pokedex_index}.png`
        },
    }
}
</script>

