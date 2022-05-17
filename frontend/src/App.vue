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
                    :task="task"
                    :locale="locale"
                    @condition="filterItems"
                    @locale="fetchItems()"
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
                <!-- Area2 for Visualization -->
                <v-col>

                    <!-- <div v-else-if="task === 'retrieve'">
                        <IdentifyItem
                        :item="detail"
                        :locale="locale"
                        @counter="counter"
                        />
                    </div> -->
                    <div>
                        <RetrieveCounter :locale="locale"/>
                    </div>
                </v-col>
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
            task : "",
            locale : "en",
            filteredItems : [],
            searched : [],
            detail : {data : {}, filteredMoves : []},
            filter : {},
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
            //arr1이 
            if (pokemonsTypes.length < filterTypes.length){
                return false
            } else {
                let type_indices = [] 
                for (let i in pokemonsTypes){
                    type_indices.push(pokemonsTypes[i].type_index)
                }
                type_indices.sort()
                filterTypes.sort()
                let idx_string = type_indices.join(' ')
                let cond_string = filterTypes.join(' ')
                if (idx_string === cond_string){
                    return true
                } else if (idx_string.includes(cond_string)) { 
                    return true
                } else {
                    return false
                }
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
            filtered = filtered.filter(el => el.is_legendary === cond.IsLegendary)
            filtered = filtered.filter(el => el.is_mythical === cond.IsMythical)
            filtered = filtered.filter(el => this.contain(el.types, cond.selectedTypes))
            this.filteredItems = filtered
            if (this.filteredItems.length === 0){
                alert('No Items')
            }
            this.filter = cond
        },
        

    

        counter : function(c){
            c;
            this.task = 'counter'
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
        },

        task : function(){
            this.filteredItems = []
            this.keyword = ""
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
