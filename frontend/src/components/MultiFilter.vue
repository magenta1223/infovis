<template>
    <div style="width:100%">
        <!-- locale select
            vuetify component for select
            when selected locale changed (@change), items are fetched (at App.vue)
        -->
        <v-row>
            <v-select
            item-text="text"
            itme-value="value"
            :items="Locales"
            v-model="selectedLocale.value"
            :label="locale =='en'? 'Locales' : '언어'"
            outlined
            @change="send()"
            ></v-select>
        </v-row>
        <!-- search
            vuetify component for text-input
            filter items by keyword
         -->
        <v-row>
            <v-text-field
            :label="locale =='en'? 'Search' : '검색하세요'"
            append-icon="mdi-magnify"
            v-model="keyword"

            @change="filter()"
            > 
            </v-text-field>
        </v-row>
        <v-row>
            <!-- 
                TypeFilter.vue
                
                :parameter
                - locale: locale
                - csshelper: css helper class for margin and padding.
                - multiple: allow multiple type or not

                :events & methods
                - filter: when triggered, the selectedTypes are updated 
            -->
            <TypeFilter
            :locale="locale"
            :csshelper="''"
            :multiple="true"
            @filter="addType"
            />
        </v-row>
        <v-row>
            <v-col cols = "6" class="justify-center">
                <!-- vuetify component for toggle -->
                <v-switch
                v-model="condition.IsLegendary"
                :label="locale == 'en' ? 'Legendary': '전설'"
                inset
                @change="filter()"
                ></v-switch>
            </v-col>
            <v-col cols = "6" class="justify-center">
                <!-- vuetify component for toggle-->
                <v-switch
                v-model="condition.IsMythical"
                :label="locale == 'en' ? 'Mythical': '환상'"
                inset
                @change="filter()"
                ></v-switch>
            </v-col>
        </v-row>
        <!--
            StatSlider 

            :parameter
            - stat: name of stat
            - vertical: vertical slider or not
            - max: max value of the slider

            event & methods
            - input: when the value changes, reflect the value to the corresponding variable

        -->

        <v-row>
            <StatSlider :stat="stats[locale]['hp']" :vertical="false" :max="200" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['attack']" :vertical="false" :max="200" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['defense']" :vertical="false" :max="200" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['spattack']" :vertical="false" :max="200" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['spdefense']" :vertical="false" :max="200" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['speed']" :vertical="false" :max="200" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['total']" :vertical="false" :max="700" @input="setVal"/>
        </v-row>
    </div>
</template>


<script>
import StatSlider from './StatSlider.vue'
import TypeFilter from './TypeFilter.vue'


export default {
    data() {
        return {
            // for locale change
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
            // for search
            keyword : "",

            // for stat sliders. 
            stats : {
                "en" : {"hp" : "HP", "attack" : "ATK", "defense" : "DEF", "spattack" : "SP.ATK", "spdefense" : "SP.DEF", "speed" : "SPD", "total" : "TOTAL"},
                "ko" : {"hp" : "체력", "attack" : "공격", "defense" : "방어", "spattack" : "특수공격", "spdefense" : "특수방어", "speed" : "속도", "total" : "총합"}
            },
            // for reverse indexing 
            stats_reverse : {
                "en" : {"HP" : "hp", "ATK" : "attack", "DEF" : "defense", "SP.ATK" : "spattack", "SP.DEF" : "spdefense", "SPD" : "speed", "TOTAL" : "total"},
                "ko" : {"체력" : "hp", "공격" : "attack", "방어" : "defense", "특수공격" : "spattack", "특수방어" : "spdefense", "속도" : "speed", "총합" : "total"}
            },

            // for filter 
            condition : {
                selectedTypes : [],
                IsLegendary : true,
                IsMythical : true,
                hp : 0,
                attack : 0,
                defense : 0,
                spattack : 0,
                spdefense : 0,
                speed : 0,
                total : 0,
            }


        }
    },

    props : ['locale'],

    methods : {

        // add selected type from the TypeFilter
        addType : function(selectedTypes){
            // add
            this.condition.selectedTypes = selectedTypes
            // vaildate
            this.typeValidator()
            // filter
            this.filter()
        },

        typeValidator : function() {
            if (this.condition.selectedTypes.length > 2) {
                this.condition.selectedTypes.pop()
                if (this.locale == 'en'){
                    alert('The pokemon can have multiple types up to 2.')
                } else {
                    alert('각 포켓몬은 최대 2개까지 타입을 가질 수 있습니다.')
                }
            } 
        },
        
        // set condition for stat
        setVal : function(newVal){
            this.condition[this.stats_reverse[this.locale][newVal.stat]] = newVal.value
            // and filter
            this.filter()
        },
        
        // triggers the method (setLocale) bind at @localeChange 
        send : function() {
            this.$emit('localeChange', this.selectedLocale.value)
        },

        // triggers the method (filterItems) bind at @condition
        filter : function(){
            this.typeValidator()
            this.$emit('condition',
                {
                    condition :  this.condition,
                    keyword : this.keyword
                })
        },
        
        // initialize condition
        initialize : function(){
            this.condition =  {
                selectedTypes : [],
                IsLegendary : true,
                IsMythical : true,
                hp : 0,
                attack : 0,
                defense : 0,
                spattack : 0,
                spdefense : 0,
                speed : 0,
                total : 0,

            }
        }
    },

    components : {
        StatSlider,
        TypeFilter
    },

    watch : {
        // when locale changed, initialize condition
        locale : function(){
            this.initialize()
        }
    },

}
</script>
