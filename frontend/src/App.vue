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
    <v-app class="container ma-0" fluid>
        <v-container>
            <v-row>
                <v-col cols="3" class="sidebar">
                    <v-row>
                        <SelectLocale
                        @locale="setLocale"
                        />
                    </v-row>
                    <v-row>
                        <v-expansion-panels>
                            <!-- Search & Retrieve -->
                            <v-expansion-panel>
                                <!-- Header -->
                                <v-expansion-panel-header @click="task='retrieve'">
                                    <template v-slot:default>
                                        Retrieve
                                    </template>
                                </v-expansion-panel-header>
                                <!-- Content -->
                                <v-expansion-panel-content>
                                    <!-- search bar -->
                                    <v-row>
                                        <SearchBar
                                        :task="task"
                                        @search="searchItems"
                                        />
                                    </v-row>
                                    <!-- items -->
                                    <v-row>
                                        <v-container >
                                            <v-row v-for="item in tableItems" :key="item.id">
                                                <v-col class = "title" v-ripple>
                                                    <v-card-title class="text-start" @click="retrieve(item.id)">
                                                        {{item.name}}
                                                    </v-card-title>
                                                    <v-divider></v-divider>
                                                </v-col>
                                            </v-row>       
                                        </v-container>
                                    </v-row>
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                            <!-- Filters -->
                            <v-expansion-panel>
                                <!-- Header -->
                                <v-expansion-panel-header @click="task='filter'">
                                    <template v-slot>
                                        Filter
                                    </template>
                                </v-expansion-panel-header>
                                <!-- Content -->
                                <v-expansion-panel-content>
                                    <!-- filters -->
                                    <MultiFilter
                                    :task="task"
                                    :locale="locale"
                                    @condition="filterItems"
                                    />
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-row>
                </v-col>
                <!-- Area2 for Visualization -->
                <v-col>
                    <div v-if="task === ''">
                        initail vue
                    </div>
                    <div v-else-if="task === 'retrieve'">
                        <IdentifyItem
                        :item="detail"
                        :locale="locale"
                        @counter="counter"
                        />
                    </div>
                    <div v-else-if="task === 'filter'">
                        <FilterCond
                        :items="filteredItems"
                        :locale="locale"
                        />
                    </div>
                    <div v-else>
                        <RetrieveCounter :locale="locale"/>
                    </div>

                </v-col>
            </v-row>
        </v-container>

    </v-app>

</template>

<script>
import MultiFilter from './components/MultiFilter.vue'
import SearchBar from './components/SearchBar.vue'
import SelectLocale from './components/SelectLocale.vue'

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
        SearchBar,
        SelectLocale,
        IdentifyItem,
        FilterCond,
        RetrieveCounter
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
                console.log(response.data)
                this.detail = response.data
                this.task = 'retrieve'
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

        filterItems : function(filter){
            
            let filtered = []

            filtered = this.items.filter(el => el.hp >= filter.hp)
            filtered = filtered.filter(el => el.attack >= filter.attack)
            filtered = filtered.filter(el => el.defense >= filter.defense)
            filtered = filtered.filter(el => el.spattack >= filter.spattack)
            filtered = filtered.filter(el => el.spdefense >= filter.spdefense)
            filtered = filtered.filter(el => el.speed >= filter.speed)
            filtered = filtered.filter(el => el.total >= filter.total)
            filtered = filtered.filter(el => el.is_legendary === filter.IsLegendary)
            filtered = filtered.filter(el => el.is_mythical === filter.IsMythical)
            filtered = filtered.filter(el => this.contain(el.types, filter.selectedTypes))
            this.filteredItems = filtered
            if (this.filteredItems.length === 0){
                alert('No Items')
            }
            this.filter = filter
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
                console.log(newVal, oldVal)
                this.fetchItems()
            },
            immediate : true
        },

        task : function(){
            this.filteredItems = []
            this.keyword = ""
        }
    },

    computed : {
        tableItems : function() {
            console.log('computed')
            if (this.searched.length > 0){
                return this.searched
            } else {
                return this.items
            }
        }
    }



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
