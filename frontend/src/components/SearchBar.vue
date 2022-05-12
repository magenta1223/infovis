<template>
    <v-row>
        <v-col>
            <v-text-field
            label="검색하세요"
            append-icon="mdi-magnify"
            v-model="keyword"

            @change="search()"
            > 
            </v-text-field>
        </v-col>
    </v-row>
</template>


<script>

export default {
    data() {
        return {
            keyword : ""
        }
        
    },

    props : ['task'],
    methods : {
        search : function(){
            this.$emit('search', this.keyword)
        }
    },

    watch : {
        task : function(){
            this.keyword = ""
        }
        }
    }

</script>
