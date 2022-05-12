<template>
    <v-container >
        <v-row v-for="item in items" :key="item.id">
            <v-col class = "title" v-ripple>
                <v-card-title class="text-start" @click="retrieve(item.id)">
                    {{item.name}}
                </v-card-title>
                <v-divider></v-divider>
            </v-col>
        </v-row>       
    </v-container>
</template>

<script>
import axios from 'axios'

let url = 'http://localhost:8000/api/pokemon/'

export default {
    
    data : () => {
        return {


            }
        },
    props: ["items", "locale"],

    methods : {

        retrieve : function(id){
            
            axios({
                method : "GET",
                url : url + id,
                params : {
                    locale : this.locale
                }
            }).then((response) => {
                this.$emit('retrieve', response.data)
            })
        }

    },
    
    watch: { 

    },

    }


</script>

<style scoped>
    .btn-containter{
        margin-top: 0;
        align-content: center;
    }

    .btn{
        margin-left: auto;
    }
.posting-container{
    margin-bottom: auto;
}


</style>