<template>
    <v-app class="container ma-2" fluid>
        <v-container class="ma-2">
            <!--
                    v-model
                    format v-model="variable"
                    bidirective binding. 
                    
                    v-bind
                    format :parameter="variable"
                        unidirective bind. send the variable of the parent component as the parameter
                        e.g. :item="detail" means send the variable named "detail" to the child component and the child assign "detail" to "item"
                    
                    emit
                    format @EVENT="METHOD"
                        eventlistener for child components
                        when EVENT occurs in the children components (MultiFilter, FilterCond ..), run METHOD
            -->

            <v-row>
                <!-- 
                    MultiFilter.vue
                    
                    paramter
                    -locale
                    
                    events & methods
                    - condition: when condition changed, filter items. multicoordinates chart in FilterCond will be changed by the "filteredItems"
                    - localeChange: when locale changed, set "locale". Every components influenced by the "locale" changing immediately
                    -->
                <v-col cols="2">
                    <MultiFilter
                    :locale="locale"
                    @condition="filterItems"
                    @localeChange="setLocale"
                    />
                </v-col>
                <!--
                    FilterCond.vue (TASK 2)
                    
                    parameter
                    - items: items filtered by conditions from MultiFilter
                    - locale: locale selected by MultiFilter

                    events & methods
                    - retrieve: when item selected, view the detail information of the item. 
                -->
                <v-col cols="6">
                    <FilterCond
                        :items="filteredItems"
                        :locale="locale"
                        @retrieve="retrieve"
                        />
                </v-col>
                <!--
                    IdentifyItem.vue (TASK 1)
                    
                    parameter
                    - item: selected item from FilterCond
                    - locale: locale selected by MultiFilter

                    events & methods
                    - 
                -->
                <v-col>
                    <IdentifyItem
                    :item="detail"
                    :locale="locale"
                    />
                </v-col>
            </v-row>
            <v-row>
                <!--
                    find counter button
                    - only appeared when selected item is fully-grown
                    - computation cost & delay
                    - items not fully-grown is rarely used in the battle.
                -->
                <v-btn v-if="!detail.data.isBaby" @click="counter()">{{ locale === 'en' ? 'find counter' : '카운터 찾기'}}</v-btn>
            </v-row>

            <v-row>
                <!--
                    RetrieveCounter.vue (TASK 3)
                    
                    parameter
                    - locale: locale selected by MultiFilter
                    - items: the counters of the item selected in FilterCond from the server 

                    events & methods
                    - 
                -->

                <RetrieveCounter
                :locale="locale"
                :items="counters"/>

            </v-row>
        </v-container>

    </v-app>

</template>

<script>
// load components
import MultiFilter from './components/MultiFilter.vue'
import IdentifyItem from './components/IdentifyItem.vue'
import FilterCond from './components/FilterCond.vue'
import RetrieveCounter from './components/RetrieveCounter.vue'
// for asynchronous communication
import axios from "axios";


// backend base url
localStorage.setItem('url', "http://127.0.0.1:8000/api/")

export default {

    // works as the variable in vanilla js. you can use these variables in the html <template>
    data(){
        return {
            // default 
            items : [],
            locale : "en",
            filteredItems : [],
            detail : {data : {}, filteredMoves : []},
            filter : {},
            counters : []
        }
    },
    
    // components to use in the template
    components : {
        MultiFilter,
        FilterCond,
        RetrieveCounter,
        IdentifyItem
    },
    
    // js functions. 
    methods : {

        // set locale
        setLocale : function(selectedLocale) {
            this.locale = selectedLocale
            console.log('locale', this.locale)
        },

        // get items by locale
        fetchItems : function(){
            // request items to server
            axios({
                method: "GET",
                url : localStorage.getItem('url') + 'pokemon/',
                params:{
                    locale : this.locale
                }
            }).then( (response) => {
                // communication success
                this.items = response.data
                console.log('items', this.items)
            }).catch((response) => {
                // communication failed
                console.log('Failed', response)
            })
        },

        // get detailed information of selected item in FilterCond
        retrieve : function(id){
            axios({
                method : "GET",
                url : localStorage.getItem('url') + 'pokemon/' + id,
                params : {
                    locale : this.locale
                }
            }).then((response) => {
                this.detail = response.data
            })
        },

        // utility function for contain relation 
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

        // filter items by condition from MultiFilter
        filterItems : function(condition){

            let keyword = condition.keyword
            let cond = condition.condition
            
            let filtered = []
            // filter by keyword
            if (keyword !== ""){
                filtered = this.items.filter(el => el.name.includes(keyword))
            } else {
                filtered = this.items
            }
            // filter by condition
            filtered = filtered.filter(el => el.hp >= cond.hp)
            filtered = filtered.filter(el => el.attack >= cond.attack)
            filtered = filtered.filter(el => el.defense >= cond.defense)
            filtered = filtered.filter(el => el.spattack >= cond.spattack)
            filtered = filtered.filter(el => el.spdefense >= cond.spdefense)
            filtered = filtered.filter(el => el.speed >= cond.speed)
            filtered = filtered.filter(el => el.total >= cond.total)
            filtered = filtered.filter(el => cond.IsLegendary? true: !el.is_legendary)
            filtered = filtered.filter(el => cond.IsMythical? true: !el.is_mythical)
            filtered = filtered.filter(el => this.contain(el.types, cond.selectedTypes))
            this.filteredItems = filtered

            // when no items
            if (this.filteredItems.length === 0){
                alert('No Items')
            }
            this.filter = cond
        },
        
        // get counters of selected item from FilterCond
        counter : function(){
            axios({
                method : "GET",
                url :  localStorage.getItem('url') + "counter/",
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
    
    // when the page is loaded, following codes will be executed
    mounted() {
        this.fetchItems()
        this.filteredItems = []
    },

    // eventlisteners for the variable in the data()
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
