<template>
    <v-select
    v-model="selectedTypes"
    :class="csshelper"
    item-text="name"
    item-value="type_index"
    :items="types"
    attach
    chips
    label="Types"
    :multiple="multiple"
    :menu-props="{ top: false, offsetY: true }"
    @change="send()"
    >
        <template #selection="{ item }">
            <v-chip :color="item.color">{{item.name}}</v-chip>
        </template>
    </v-select>

</template>


<script>
import axios from 'axios'


export default {
    data() {
        return {
            selectedTypes : [],
            types : [],
        }  
    },

    props : ['locale', 'multiple', 'csshelper'],

    methods : {
        fetchTypes : function() {
            // get types by locale from the backend
            axios({
                method : "GET",
                url : 'http://127.0.0.1:8000/api/poketype/',
                params : {
                    locale : this.locale
                }
            }).then( (response) => {
                this.types = response.data
            }).catch((response) => {
                console.log('Failed', response)
            })
        },

        send : function(){
            this.$emit('filter', this.selectedTypes)
        }
        
    },

    mounted() {
        this.fetchTypes()
    },

    watch : {
        locale : function(){
            this.fetchTypes()
        } 
    }
}
</script>
