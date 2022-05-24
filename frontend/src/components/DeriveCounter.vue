<template>
<v-container id="Rcontainer">
    <v-row>
        <v-col>
            <!-- vuetify component for select -->
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

    <!-- bar chart -->
    <v-row>
        <svg id="bar"></svg>
    </v-row>

    <div id="tooltipR">
        <div class = "tooltip">
            dddd
        </div>
    </div>

    
</v-container>
</template>


<script>
import BarChart from "../d3Chart/barchart.js"
import * as d3 from "d3";

export default {
    data: () => {
        return {
            // orders for sort the bar chart
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

    props : ['items', 'locale'],


    mounted() {
        // initialize chart
        this.barchart = new BarChart("#bar", 1800, 600)
        this.barchart.initialize()

        // render chart by selected order
        this.barchart.update(this.items, this.selectedOrder.value)

        // add eventlistener
        this.barchart.rects.on("click", e => {
            // when line clicked, highlight the item
            this.selected = e.srcElement.__data__
            this.barchart.highlight(this.selected)
        })
        
        // add eventlistener
        d3.select("#Rcontainer").on("click",e => {
            // when clicked element's tag is not rect or text
            // off the highlight
            if (e.target.tagName !== "rect" & e.target.tagName !== "text") {
                console.log('off')
                this.barchart.off()
            }
        });
    },

    watch : {
        // when items changed, barchart is updated
        items : function(){
            this.barchart.update(this.items, this.selectedOrder.value)
        },
        
        // when selectedOrder changed, barchart is updated
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
    .tooltip {
        width : auto;
        visibility: hidden;
        background: #333;
        color: white;
        font-weight: bold;
        padding: 4px 8px;
        font-size: 13px;
        border-radius: 4px;
    }

</style>