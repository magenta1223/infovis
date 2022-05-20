<template>
<div style="width:100%">
    <v-row>
        <v-col class="text-center">
            {{stat}}
        </v-col>
    </v-row>
    <v-row>
        <v-slider
            v-model="value"
            :vertical="vertical"
            thumb-label
            step="5"
            @change="onChanged"
            max=200
            >
        </v-slider>
    </v-row>
</div>

</template>

<script>
export default {
    data() {
        return {
            value : 0
        }
    },

    props : ['stat', 'vertical'],

    methods : {
        onChanged : function(){
            console.log(this.stat )
            this.$emit(
                'input',
                {
                    stat : this.stat,
                    value : this.value
                }
            )
        }
    },


}
</script>
