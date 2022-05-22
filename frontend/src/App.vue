<template>
<!-- plan
1) search bar
2) filter
3) lists
4) vis
총 4개의 영역으로 구성하고
vis part는 router로 구성함
전부 비동기로 작동
 -->
    <v-app class="container ma-2" fluid>
        <v-container class="ma-2">
            <v-row>
                <v-col cols="2">
                    <MultiFilter
                    :locale="locale"
                    @condition="filterItems"
                    @localeChange="setLocale"
                    />
                </v-col>
                <v-col cols="6">
                    <FilterCond
                        :items="filteredItems"
                        :locale="locale"
                        @retrieve="retrieve"
                        />
                </v-col>
                <v-col>
                    <IdentifyItem
                    :item="detail"
                    :locale="locale"
                    />
                </v-col>
            </v-row>
            <v-row>
                <v-btn v-if="!detail.data.isBaby" @click="counter()">{{ locale === 'en' ? 'find counter' : '카운터 찾기'}}</v-btn>
            </v-row>

            <v-row>
                <!-- Area2 for Visualization -->

                <RetrieveCounter :locale="locale" :items="counters"/>

            </v-row>
        </v-container>

    </v-app>

</template>

<script>
import MultiFilter from './components/MultiFilter.vue'
import IdentifyItem from './components/IdentifyItem.vue'
import FilterCond from './components/FilterCond.vue'
import RetrieveCounter from './components/RetrieveCounter.vue'
import axios from "axios";


let url = "http://127.0.0.1:8000/api/pokemon/"

export default {
    data(){
        return {
            items : [{id : 1}, {id : 2}],
            locale : "en",
            filteredItems : [],
            searched : [],
            detail : {data : {}, filteredMoves : []},
            filter : {},
            counters : []
        }
    },

    components : {
        MultiFilter,
        FilterCond,
        RetrieveCounter,
        IdentifyItem
    },

    methods : {
        setLocale : function(selectedLocale) {
            this.locale = selectedLocale
            console.log('locale', this.locale)

        },

        fetchItems : function(){
            axios({
                method: "GET",
                url : url,
                params:{
                    locale : this.locale
                }
            }).then( (response) => {
                this.items = response.data
                console.log('items', this.items)
            }).catch((response) => {
                console.log('Failed', response)
            })
        },

        retrieve : function(id){
            axios({
                method : "GET",
                url : url + id,
                params : {
                    locale : this.locale
                }
            }).then((response) => {
                this.detail = response.data
            })
        },

        searchItems : function(keyword){
            this.searched = this.items.filter(el => el.name.includes(keyword))
        },

        contain : function(pokemonsTypes, filterTypes) {
            if (filterTypes.length === 0){
                return true
            }
            //required types > element's type
            if (pokemonsTypes.length < filterTypes.length){
                return false
            } else {
                // if not, required length <= element's length
                let type_indices = pokemonsTypes.map(d => d.type_index)
                for (let i in filterTypes){
                    if (!(type_indices.includes(filterTypes[i]))){
                        return false
                    }
                }
                return true

            }
        },

        filterItems : function(condition){

            let keyword = condition.keyword
            let cond = condition.condition
            
            let filtered = []
            if (keyword !== ""){
                filtered = this.items.filter(el => el.name.includes(keyword))
            } else {
                filtered = this.items
            }
            filtered = filtered.filter(el => el.hp >= cond.hp)
            filtered = filtered.filter(el => el.attack >= cond.attack)
            filtered = filtered.filter(el => el.defense >= cond.defense)
            filtered = filtered.filter(el => el.spattack >= cond.spattack)
            filtered = filtered.filter(el => el.spdefense >= cond.spdefense)
            filtered = filtered.filter(el => el.speed >= cond.speed)
            filtered = filtered.filter(el => el.total >= cond.total)
            filtered = filtered.filter(el => cond.IsLegendary? el.is_legendary: true)
            filtered = filtered.filter(el => cond.IsMythical? el.is_mythical: true)
            filtered = filtered.filter(el => this.contain(el.types, cond.selectedTypes))
            this.filteredItems = filtered
            if (this.filteredItems.length === 0){
                alert('No Items')
            }
            this.filter = cond
        },
        
        counter : function(){
            axios({
                method : "GET",
                url : "http://127.0.0.1:8000/api/counter/",
                params : {
                    locale : this.locale,
                    pokedex_index : this.detail.data.pokedex_index
                }
            }).then(response => {
                this.counters = response.data
            }).catch(response => {
                console.log("Failed", response)
            })

        }

    },


    mounted() {
        this.fetchItems()
        this.filteredItems = []
    },

    watch : {
        locale : {
            handler(newVal, oldVal){
                newVal;oldVal; // eslint
                this.fetchItems()
            },
            immediate : true
        }
    },

}
</script>



<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.container {
    max-width: 1920px;
}


.sidebar {
    margin : 40px;
}

</style>
