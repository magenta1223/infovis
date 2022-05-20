<template>
<div>
    <v-select
    item-text="text"
    itme-value="value"
    :items="orders"
    v-model="selectedOrder.value"
    label="Orders"
    outlined
    ></v-select>
    
    <svg id="bar">
    </svg>
</div>
</template>


<script>
import BarChart from "../d3Chart/barchart.js"

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

    methods : {
        
    },

    mounted() {
        this.barchart = new BarChart("#bar", 1000, 600)
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