<template>
<div style="width:100%">
    <v-row>
        <!-- stat name -->
        <v-col class="text-center">
            {{stat}}
        </v-col>
    </v-row>
    <v-row>
        <!-- vuetify component for slider -->
        <v-slider
            v-model="value"
            :vertical="vertical"
            thumb-label
            step="5"
            @change="onChanged"
            :max="max"
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

    props : ['stat', 'vertical', 'max'],

    methods : {
        // triggers the method(setVal) bind at @input of parent component
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
