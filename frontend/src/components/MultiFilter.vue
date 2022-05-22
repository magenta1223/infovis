<template>
<!-- type, stat, 전포 환포 -->
    <div style="width:100%">
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
            <TypeFilter
            :locale="locale"
            :csshelper="''"
            :multiple="true"
            @filter="addType"
            />
        </v-row>
        <v-row>
            <v-col cols = "6" class="justify-center">
                <v-switch
                v-model="IsLegendary"
                :label="locale == 'en' ? 'Legendary': '전설'"
                inset
                @change="filter()"
                ></v-switch>
            </v-col>
            <v-col cols = "6" class="justify-center">
                <v-switch
                v-model="IsMythical"
                :label="locale == 'en' ? 'Mythical': '환상'"
                inset
                @change="filter()"
                ></v-switch>
            </v-col>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['hp']" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['attack']" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['defense']" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['spattack']" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['spdefense']" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['speed']" :vertical="false" @input="setVal"/>
        </v-row>
        <v-row>
            <StatSlider :stat="stats[locale]['total']" :vertical="false" @input="setVal"/>
        </v-row>
    </div>
</template>


<script>
import StatSlider from './StatSlider.vue'
import TypeFilter from './TypeFilter.vue'


export default {
    data() {
        return {
            // for locales
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
            stats : {
                "en" : {"hp" : "HP", "attack" : "ATK", "defense" : "DEF", "spattack" : "SP.ATK", "spdefense" : "SP.DEF", "speed" : "SPD", "total" : "TOTAL"},
                "ko" : {"hp" : "체력", "attack" : "공격", "defense" : "방어", "spattack" : "특수공격", "spdefense" : "특수방어", "speed" : "속도", "total" : "총합"}
            },

            // for filter
            selectedTypes : [],
            IsLegendary : false,
            IsMythical : false,
            hp : 0,
            attack : 0,
            defense : 0,
            spattack : 0,
            spdefense : 0,
            speed : 0,
            total : 0,

        }
    },

    props : ['locale'],

    methods : {
        addType : function(selectedTypes){
            this.selectedTypes = selectedTypes
            this.limiter()
            this.filter()
        },

        limiter : function() {

            if (this.selectedTypes.length > 2) {
                this.selectedTypes.pop()
                if (this.locale == 'en'){
                    alert('The pokemon can have multiple types up to 2.')
                } else {
                    alert('각 포켓몬은 최대 2개까지 타입을 가질 수 있습니다.')
                }
            } 
        },

        setVal : function(newVal){
            // hard coding >> soft
            let stat = newVal.stat
            if (stat === "HP"){
                this.hp = newVal.value
            } else if (stat === "ATK"){
                this.attack = newVal.value
            } else if (stat === "DEF"){
                this.attack = newVal.value
            } else if (stat === "SP.ATK"){
                this.spattack = newVal.value
            } else if (stat === "SP.DEF"){
                this.spattack = newVal.value
            } else if (stat === "SPD"){
                this.speed = newVal.value
            } else {
                this.total = newVal.value
            }
            this.filter()
        },

        send : function() {
            console.log('filter',  this.selectedLocale.value)
            this.$emit('localeChange', this.selectedLocale.value)
        },

        filter : function(){
            this.limiter()
            this.$emit('condition',
                {
                    condition :  this.condition,
                    keyword : this.keyword
                })
        },

        initialize : function(){
            this.selectedTypes = []
            this.IsLegendary = false
            this.IsMythical = false
            this.hp = 0
            this.attack = 0
            this.defense = 0
            this.spattack = 0
            this.spdefense =0
            this.speed = 0
            this.total = 0
        }
    },

    components : {
        StatSlider,
        TypeFilter
    },

    watch : {
        locale : function(){
            this.initialize()
        }
    },


    computed : {
        condition : function(){
            return {
                hp : this.hp,
                attack : this.attack,
                defense : this.defense,
                spattack : this.spattack,
                spdefense : this.spdefense,
                speed : this.speed,
                total : this.total,
                IsLegendary : this.IsLegendary,
                IsMythical : this.IsMythical,
                selectedTypes : this.selectedTypes
                }
        }
    }




}
</script>
