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
                <v-col cols="5" class="sidebar">
                    <v-row>
                        <SelectLocale
                        @locale="setLocale"
                        />
                    </v-row>
                    <v-row>
                        <v-expansion-panels>
                            <v-expansion-panel>
                            
                                <v-expansion-panel-header @click="task='retrieve'">
                                    <template v-slot:default>
                                        Retrieve
                                    </template>
                                </v-expansion-panel-header>
                                <v-expansion-panel-content>
                                    <SearchBar
                                    :task="task"
                                    @search="searchItems"
                                    />
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                            <v-expansion-panel>
                                <v-expansion-panel-header @click="task='filter'">
                                    <template v-slot>
                                        Filter
                                    </template>
                                </v-expansion-panel-header>
                                <v-expansion-panel-content>
                                    <MultiFilter
                                    :task="task"
                                    :locale="locale"
                                    @condition="filterItems"
                                    />
                                </v-expansion-panel-content>
                            </v-expansion-panel>
                        </v-expansion-panels>
                    </v-row>
                    <v-row>
                        <ListItem
                        :items="tableItems"
                        :locale="locale"
                        @retrieve="retrieveItem"
                        />

                    </v-row>
                </v-col>
                <v-col cols="6">
                    <div v-if="task === ''">
                        initail vue
                    </div>
                    <div v-else-if="task === 'retrieve'">
                        <IdentifyItem
                        :item="detail"
                        />
                    </div>
                    <div v-else-if="task === 'filter'">
                        <FilterCond/>
                    </div>
                    <div v-else>
                        <RetrieveCounter/>
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
import ListItem from './components/ListItem.vue'

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
            detail : {},
            filter : {}
        }
    },

    components : {
        MultiFilter,
        SearchBar,
        SelectLocale,
        ListItem,
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
        searchItems : function(keyword){
            console.log(keyword)
            this.filteredItems = this.items.filter(el => el.name.includes(keyword))
            console.log(this.task)
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
        
        retrieveItem : function(item){
            this.detail = item
            this.task = 'retrieve'
        },
        
        refetchByLocale : function(){
            this.fetchItems()
            console.log(this.task)
            if (this.task === "retrieve"){
                this.searchItems()
            } else if (this.task === "filter"){
                this.filterItems(this.filter)
                console.log('여기 무자식아', this.items)
            }
            
        }

    },


    mounted() {
        this.fetchItems()
        this.filteredItems = []
    },

    watch : {
        // locale : function() {
        //     this.fetchItems()
        //     this.filteredItems = []
        // },


        locale : {
            handler(newVal, oldVal){
                console.log(newVal, oldVal)
                this.refetchByLocale()
                
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
            if (this.filteredItems.length > 0){
                return this.filteredItems
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
