<template>
    <v-select
    item-text="text"
    itme-value="value"
    :items="Locales"
    v-model="selectedLocale.value"
    label="Locales"
    outlined
    @change="send()"
    ></v-select>
</template>

<script>

export default {
    data() {
        return {
            selectedLocale: {
                    text : 'English',
                    value : 'en'
            },
            Locales: [
                {
                    text : 'English',
                    value : 'en'
                },
                {
                    text : '한국어',
                    value : 'ko'
                }
            ],
        }
    },

    methods : {
        send : function() {
            this.$emit('locale', this.selectedLocale.value)
        }

    }
}
</script>
