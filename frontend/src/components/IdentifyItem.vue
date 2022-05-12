<template>
    <div>
        {{item.hp}}
        <div id="canvas"></div>
        <svg id="radar"></svg>
    </div>


</template>


<script>
import RadarChart from '../d3Chart/radar.js'

export default {
    data() {
        return {
            items : [],
            features : ["A","B","C","D","E","F"],
            radarchart : "#radar"
            
        }
    },

    components : {
        
    },


    props : ['item'],

    methods :{




    },

    mounted() {
        for (let i = 0; i < 3; i++){
            let point = {}
            //each feature will be a random number from 1-9
            this.features.forEach(f => point[f] = 100 + Math.random() * 50);
            this.items.push(point);
        }
        
        this.radarchart = new RadarChart(this.radarchart, this.features)
        this.radarchart.initialize()
        this.radarchart.update(this.items)

        
        
        //Call function to draw the Radar chart
        //RadarChart(
        //      "id or class of to which the new SVG needs to be appended",
        //      the dataset,
        //      the options (optional))


    }
}
</script>


<style>
    body {
        font-family: 'Open Sans', sans-serif;
        font-size: 11px;
        font-weight: 300;
        fill: #242424;
        text-align: center;
        text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff, 0 -1px 0 #fff;
        cursor: default;
    }

    .legend {
        font-family: 'Raleway', sans-serif;
        fill: #333333;
    }

    .tooltip {
        fill: #333333;
    }
</style>


