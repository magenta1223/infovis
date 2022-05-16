<template>
    <div style="width:100%">
        <!--item이 15개 이상이면 위에 경고메세지 같은거 -->
        <v-row>
            <v-col>
                <svg id="polycoords"></svg>
            </v-col>
        </v-row>
        <v-row>

            <v-col>
                <v-data-table
                    :headers="headers[locale]"
                    :items="items"
                    class="elevation-1"
                >
                <template v-slot:[`item.types`]="{ item }">
                    <v-chip v-for="type in item.types" :key="type.id" :color="type.color" small class="ma-1">{{type.name}}</v-chip>
                </template>
                </v-data-table>
            </v-col>
        </v-row>
    </div>
</template>


<script>
import MultiCoordinates from "../d3Chart/multicoordinates.js"


//let spriteUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/'

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
                    {text : 'HP', value : 'hp'},
                    {text : 'Attack', value : 'attack'},
                    {text : 'Defense', value : 'defense'},
                    {text : 'SP.Attack', value : 'spattack'},
                    {text : 'SP.Defense', value : 'spdefense'},
                    {text : 'Speed', value : 'speed'},
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
                    {text : '타입', value : 'type'}
                ]
            },

        }
    },

    props : ['items', 'locale'],
    mounted() {

        console.log('filter mount', this.items)
        this.multicoords = new MultiCoordinates("#polycoords", this.features[this.locale], 1200, 280)
        this.multicoords.initialize()
        this.multicoords.update(this.items)

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
        items : function(){
            console.log(this.selected)
            this.multicoords.update(this.items)
        }
    },




}
</script>
