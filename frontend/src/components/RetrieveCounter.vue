<template>
<v-container>
    <v-row>
        <v-col>
            <v-select
            item-text="text"
            itme-value="value"
            :items="orders"
            v-model="selectedOrder.value"
            label="Orders"
            outlined
            ></v-select>
        </v-col>
        <v-col>
            <TypeFilter
            :locale="locale"
            :csshelper="''"
            :multiple="false"
            @filter="filter"
            />
        </v-col>
    </v-row>

    <v-row>
        <svg id="bar"></svg>
    </v-row>
</v-container>
</template>


<script>
import BarChart from "../d3Chart/barchart.js"
import TypeFilter from './TypeFilter.vue'

export default {
    data: () => {
        return {
            selectedOrder: {
                    text : 'Descending',
                    value : 'desc'
            },
            orders: [
                {
                    text : 'Descending',
                    value : 'desc'
                },
                {
                    text : 'Ascending',
                    value : 'asc'
                },
                {
                    text : 'Type',
                    value : 'type'
                }
            ],
        }
    },

    props : ['item', 'locale'],

    components:{
        TypeFilter
    },

    methods : {
        filter : function(selectedType){

            this.item.filter(e => e.)

        }
        
    },

    mounted() {
        this.barchart = new BarChart("#bar", 1800, 600)
        this.barchart.initialize()
        this.barchart.update(this.item, this.selectedOrder.value)
    },

    watch : {
        item : function(){
            this.barchart.update(this.item, this.selectedOrder.value)
        },

        selectedOrder : {
            handler(newVal, oldVal){
                oldVal; // eslint
                this.barchart.update(this.item, newVal.value)
            },
            immediate : true,
            deep : true
        }
    }
}
</script>


<style scoped>
.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 2px;
}
</style>