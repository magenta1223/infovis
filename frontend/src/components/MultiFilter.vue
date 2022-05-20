<template>
<!-- type, stat, 전포 환포 -->
    <div style="width:100%">
        <v-row>
            <v-select
            item-text="text"
            itme-value="value"
            :items="Locales"
            v-model="selectedLocale.value"
            label="Locales"
            outlined
            @change="send()"
            ></v-select>
        </v-row>
        <v-row>
            <v-text-field
            label="검색하세요"
            append-icon="mdi-magnify"
            v-model="keyword"

            @change="filter()"
            > 
            </v-text-field>
        </v-row>
        <v-row>
            <v-select
            v-model="selectedTypes"
            item-text="name"
            item-value="type_index"
            :items="items"
            attach
            chips
            label="Types"
            multiple
            :menu-props="{ top: false, offsetY: true }"
            @change="filter()"
            >
            <template #selection="{ item }">
                <v-chip :color="item.color">{{item.name}}</v-chip>
            </template>

            </v-select>
        </v-row>
        <v-row>
            <v-col cols = "6" class="justify-center">
                <v-switch
                v-model="IsLegendary"
                label="legendary"
                inset
                @change="filter()"
                ></v-switch>
            </v-col>
            <v-col cols = "6" class="justify-center">
                <v-switch
                v-model="IsMythical"
                label="mythical"
                inset
                @change="filter()"
                ></v-switch>
            </v-col>
        </v-row>
        <v-row>
            <StatSlider :stat="'HP'" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="'ATK'" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="'DEF'" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="'SP.ATK'" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="'SP.DEF'" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="'SPD'" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="'TOTAL'" :vertical="false" @input="setVal"/>
        </v-row>
    </div>
</template>


<script>
import axios from 'axios'
import StatSlider from './StatSlider.vue'

let url = "http://127.0.0.1:8000/api/poketype/"


export default {
    data() {
        return {
            // for locales
            selectedLocale: {
                    text : 'English',
                    value : 'en'
            },
            Locales: [
                {
                    text : 'English',
                    value : 'en'
                },
                {
                    text : '한국어',
                    value : 'ko'
                }
            ],
            // for search
            keyword : "",
            // for filter
            items : [],
            selectedTypes : [],
            IsLegendary : false,
            IsMythical : false,
            hp : 0,
            attack : 0,
            defense : 0,
            spattack : 0,
            spdefense : 0,
            speed : 0,
            total : 0,

        }
    },

    props : ['locale'],

    methods : {
        fetchTypes : function() {
            axios({
                method : "GET",
                url : url,
                params : {
                    locale : this.locale
                }
            }).then( (response) => {
                console.log(response)
                this.items = response.data
                console.log(this.items)
            }).catch((response) => {
                console.log('Failed', response)
            })
        },

        limiter : function() {

            if (this.selectedTypes.length > 2) {
                this.selectedTypes.pop()
                if (this.locale == 'en'){
                    alert('The pokemon can have multiple types up to 2.')
                } else {
                    alert('각 포켓몬은 최대 2개까지 타입을 가질 수 있습니다.')
                }
            } 
        },
        setVal : function(newVal){
            let stat = newVal.stat
            if (stat === "HP"){
                this.hp = newVal.value
            } else if (stat === "ATK"){
                this.attack = newVal.value
            } else if (stat === "DEF"){
                this.attack = newVal.value
            } else if (stat === "SP.ATK"){
                this.spattack = newVal.value
            } else if (stat === "SP.DEF"){
                this.spattack = newVal.value
            } else if (stat === "SPD"){
                this.speed = newVal.value
            } else {
                this.total = newVal.value
            }
            this.filter()
        },

        send : function() {
            console.log('filter',  this.selectedLocale.value)
            this.$emit('localeChange', this.selectedLocale.value)
        },


        filter : function(){
            this.limiter()
            this.$emit('condition',
                {
                    condition :  this.condition,
                    keyword : this.keyword
                })
        },

        initialize : function(){
            this.items = []
            this.selectedTypes = []
            this.IsLegendary = false
            this.IsMythical = false
            this.hp = 0
            this.attack = 0
            this.defense = 0
            this.spattack = 0
            this.spdefense =0
            this.speed = 0
            this.total = 0
        }
    },

    components : {
        StatSlider
    },


    mounted() {
        this.fetchTypes()
    },

    watch : {
        locale : function(){
            this.fetchTypes()
            this.initialize()
        }
    },


    computed : {
        condition : function(){
            return {
                hp : this.hp,
                attack : this.attack,
                defense : this.defense,
                spattack : this.spattack,
                spdefense : this.spdefense,
                speed : this.speed,
                total : this.total,
                IsLegendary : this.IsLegendary,
                IsMythical : this.IsMythical,
                selectedTypes : this.selectedTypes
                }
        }
    }




}
</script>
