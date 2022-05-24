<template>
    <div style="width:100%">
        <!-- wrapper -->
        <v-card
        height="900"
        class="overflow-y-auto overflow-x-hidden">
            <!-- sprite & stats -->
            <v-row align="center">
                <!-- sprites -->
                <v-col cols = "5">
                    <!-- vuetify component for image -->
                    <v-img :src="imgSrc" max-width="400"  position="center"  /> 
                </v-col>
                <!-- radar chart -->
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
                <!-- 
                    TypeFilter.vue
                    
                    :parameter
                    - locale: locale
                    - csshelper: css helper class for margin and padding.
                    - multiple: allow multiple type or not

                    :events & methods
                    - filter: when triggered, the moves are filtered by types 
                 -->
                <TypeFilter
                :locale="locale"
                :csshelper="'mb-4 ml-4 mr-4'"
                :multiple="false"
                @filter="filter"
                />
            <v-row>
                <v-col>
                    <!-- vuetify component for table -->
                    <v-data-table
                        :headers="headers[locale]"
                        :items="filteredMoves"
                        class="elevation-1"
                    >
                        <!-- custom row design-->
                        <template v-slot:[`item.type`]="{ item }">
                            <v-chip :color="item.type.color" small> {{item.type.name}}</v-chip>
                        </template>
                    </v-data-table>
                </v-col>
            </v-row>
        </v-card>
        <div v-for="f in features[locale]" :key="f[0]" :id="'t'+ f[1]">
            <div class = "tooltip">
                dddd
            </div>
        </div>
        <div id="t7">
            <div class = "tooltip">
                dddd
            </div>
        </div>
    </div>




</template>


<script>
import RadarChart from '../d3Chart/radar.js'
import TypeFilter from "./TypeFilter.vue"

let spriteUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'

export default {
    data() {
        return {
            // the name and index of radar chart's each axis 
            features : {
                "en" : [['HP', 0], ['ATTACK', 1],[ 'DEFENSE', 2], ['SP.ATTACK', 3], ['SP.DEFENSE', 4], ['SPEED', 5]],
                "ko" : [['체력', 0], ['공격', 1], ['방어', 2], ['특수공격', 3], ['특수방어', 4], ['스피드', 5]]  
            },
            // headers for table
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

            // variables
            moves : [],
            selectedTypes : [],
            types : [],
            filtered : [],
            filteredMoves : [],

            defaultItem : {
                hp : 0,
                attack : 0,
                defense : 0,
                spattack : 0,
                spdefense : 0,
                speed : 0,
                types : [{color : "#000000"}]
            }
        }
    },

    components : {
        TypeFilter,
    },


    // variables from parent component 
    props : ['item', 'locale'],
    
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
        // generate chart
        this.radarchart = new RadarChart("#radar", this.features[this.locale], 200, 250)
        this.radarchart.initialize()
        this.radarchart.update(this.defaultItem)
    },

    watch : {
        // when item changed, the radar chart is updated
        item : function(){
            this.radarchart.update(this.item.data)
            this.moves = this.item.moves.map( (d) => (d.move) )
            this.filteredMoves = this.moves
        }
    },
    
    // dynamic variable
    computed : {
        imgSrc : function() {
            return `${spriteUrl}${this.item.data.pokedex_index}.png`
        },
    }
}
</script>

<style scoped>
    .tooltip {
        width : auto;
        visibility: hidden;
        background: #333;
        color: white;
        font-weight: bold;
        padding: 4px 8px;
        font-size: 13px;
        border-radius: 4px;
    }

</style>