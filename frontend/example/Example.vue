<template>
<!-- -->
    <div>
        <Other/>
        <div :var="value"> 
        </div>
    </div>

</template>

<script>
import Other from './Other.vue'


export default {
    data(){
        return {
            value : 0
        }
    },

    components :{
        Other
    }
}
</script>
