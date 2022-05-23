<template>
    <!-- vuetify component for select -->
    <v-select
    v-model="selectedTypes"
    :class="csshelper"
    item-text="name"
    item-value="type_index"
    :items="types"
    attach
    chips
    :label="locale =='en'? 'Types' : '타입'"
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
            // for selection
            selectedTypes : [],
            types : [],
        }  
    },

    props : ['locale', 'multiple', 'csshelper'],

    methods : {
        // get types from the server by locale
        fetchTypes : function() {
            axios({
                method : "GET",
                url : localStorage.getItem('url') + 'poketype/',
                params : {
                    locale : this.locale
                }
            }).then( (response) => {
                this.types = response.data
            }).catch((response) => {
                console.log('Failed', response)
            })
        },
        // when selected type changes, triggers the method of parent component bind at @filter
        send : function(){
            this.$emit('filter', this.selectedTypes)
        }
        
    },

    mounted() {
        // when loaded, get types from the server
        this.fetchTypes()
    },

    watch : {
        // when locale changed, get types from the server
        locale : function(){
            this.fetchTypes()
        } 
    }
}
</script>
