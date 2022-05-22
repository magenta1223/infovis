<template>
<v-container id="container">
    <v-row>
        <v-col>
            <v-select
            item-text="text"
            itme-value="value"
            :items="orders"
            v-model="selectedOrder.value"
            :label="locale === 'en' ?  'Orders': '정렬방법'"
            outlined
            ></v-select>
        </v-col>
    </v-row>

    <v-row>
        <svg id="bar"></svg>
    </v-row>
</v-container>
</template>


<script>
import BarChart from "../d3Chart/barchart.js"
import * as d3 from "d3";

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
            filteredItems : []
        }
    },

    props : ['items', 'locale'],

    components:{
    },

    methods : {
        
    },

    mounted() {
        this.barchart = new BarChart("#bar", 1800, 600)
        this.barchart.initialize()
        this.barchart.update(this.items, this.selectedOrder.value)
        this.barchart.rects.on("click", e => {
            console.log('rect', e.target)
            this.selected = e.srcElement.__data__
            this.barchart.highlight(this.selected)
        })
        
        d3.select("#container").on("click",e => {
            if (e.target.tagName !== "rect" & e.target.tagName !== "text") {
                console.log('off')
                this.barchart.off()
            }
        });
    },

    watch : {
        items : function(){
            this.barchart.update(this.items, this.selectedOrder.value)
        },

        selectedOrder : {
            handler(newVal, oldVal){
                oldVal; // eslint
                this.barchart.update(this.items, newVal.value)
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