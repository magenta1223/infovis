<template>
    <div style="width:100%">
        <!-- Parallel Coordinates  -->
        <v-row id="container">
            <v-col>
                <svg id="parallelCoords"></svg>
            </v-col>
        </v-row>

        <!-- table for items filtered from App.vue -->
        <v-row>
            <v-col>
                <!-- vuetify component for table -->
                <v-data-table
                    :headers="headers[locale]"
                    :items="items"
                    class="elevation-1"
                >
                    <!-- custom row design -->
                    <template v-slot:item="{ item }">
                        <!-- when clicked row, the item corresponding with the row in the chart is highlighted -->
                        <tr @click="click(item)">
                            <!-- fields -->
                            <td>{{ item.name }}</td>
                            <td>{{ item.hp }}</td>
                            <td>{{ item.attack }}</td>
                            <td>{{ item.defense }}</td>
                            <td>{{ item.spattack }}</td>
                            <td>{{ item.spdefense }}</td>
                            <td>{{ item.speed }}</td>
                            <td>{{ item.total }}</td>
                            <!-- types -->
                            <td> <v-chip v-for="type in item.types" :key="type.id" :color="type.color" small class="ma-1">{{type.name}}</v-chip> </td>
                        </tr>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </div>
</template>


<script>
import ParallelCoordinates from "../d3Chart/parallelcoordinates.js"
import * as d3 from "d3";

export default {
    data() {
        return {
            // the name and index of parallel coordinates chart's each axis 
            features : {
                "en" : [['HP', 0], ['ATTACK', 1],[ 'DEFENSE', 2], ['SP.ATTACK', 3], ['SP.DEFENSE', 4], ['SPEED', 5]],
                "ko" : [['체력', 0], ['공격', 1], ['방어', 2], ['특수공격', 3], ['특수방어', 4], ['스피드', 5]]  
            },

            // headers for table
            headers : {
                "en" : [
                    {text : 'Name', value : 'name'},
                    {text : 'HP', value : 'hp'},
                    {text : 'Attack', value : 'attack'},
                    {text : 'Defense', value : 'defense'},
                    {text : 'SP.Attack', value : 'spattack'},
                    {text : 'SP.Defense', value : 'spdefense'},
                    {text : 'Speed', value : 'speed'},
                    {text : 'Total', value : 'total'},
                    {text : 'Type', value : 'types'}

                ],
                "ko" : [
                    {text : '이름', value : 'name'},
                    {text : '체력', value : 'hp'},
                    {text : '공격', value : 'attack'},
                    {text : '방어', value : 'defense'},
                    {text : '특수공격', value : 'spattack'},
                    {text : '특수방어', value : 'spdefense'},
                    {text : '스피드', value : 'speed'},
                    {text : '총합', value : 'total'},
                    {text : '타입', value : 'type'}
                ]
            },
            
            // for highlighting
            selected : ""

        }
    },
    
    // variables from parent component (App.vue)
    props : ['items', 'locale'],

    methods : {
        // when the row clicked, highlight the item
        click : function(item){
            this.selected = item
            this.parallelCoordinates.highlight(this.selected)
            // triggers the method (retrieve) bind at @retrieve
            this.$emit("retrieve", item.id)
      }  
    },

    mounted() {
        console.log('filter mount', this.items)
        // generate chart. width / height is for 1920-1080.
        this.parallelCoordinates = new ParallelCoordinates("#parallelCoords", this.features[this.locale], 800, 280)
        this.parallelCoordinates.initialize()
        this.parallelCoordinates.update(this.items)

        // add eventlistener
        this.parallelCoordinates.lines.on("click", (e) => {
            // when line clicked, highlight the item
            this.selected = e.srcElement.__data__
            this.parallelCoordinates.highlight(this.selected)
            // triggers the method (retrieve) bind at @retrieve
            this.$emit("retrieve", this.selected.id)
        })
        // add eventlistener
        d3.select("#container").on("click",e => {
            // when clicked element's tag is not path
            // off the highlight
            if (e.target.tagName !== "path") {
                console.log('filter off')
                this.parallelCoordinates.off()
            }
        });

    },
    

    watch : {
        // when items changed, update chart
        items : function(){
            console.log(this.selected)
            this.parallelCoordinates.update(this.items)      
        }
    },




}
</script>
