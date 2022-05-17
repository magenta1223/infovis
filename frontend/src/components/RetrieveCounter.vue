<template>
    <div id="sunburst">
    </div>

</template>


<script>
import SunBurst from "../d3Chart/sunburst.js"
import data from "../d3Chart/data.json"

export default {
    data: () => {
        return {
            chart : "",
            data :data
            
        }
    },

    methods : {
        
    },

    mounted() {
        this.sunburst = new SunBurst("#sunburst", 600, 600)
        this.sunburst.initialize()
        this.sunburst.update(this.data)
    }

}

// import axios from 'axios'
// let url = 'http://localhost:8000/api/counter/'

// export default {

//     props : ['locale'],
//     mounted(){
//         console.log(url, this.locale)
//         axios({
//             method : 'GET',
//             url : url,
//             params : {
//                 pokedex_index : 1,
//                 locale : this.locale
//             }
//         }).then((response) => {
//             console.log( 'counter success', response)
//         }).catch((response) => {
//             console.log('Failed', response)
//         })
//     }
// }
</script>
