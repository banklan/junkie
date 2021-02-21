<template>
    <div class="checked_out">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12">
                    <div class="headline mb-5">Create new campaign (Step 2 of 3)</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="7">
                    <v-card light outlined min-height="200" class="px-6 py-4">
                        <v-card-title class="title justify-center mb-4 primary--text">
                            Set the goals and expiry of your campaign.
                        </v-card-title>
                        <v-card-text align="start">
                            <v-text-field label="Goal(Naira)" hint="How much are you looking to raise? Enter figure without commas" v-model="create.goal" required v-validate="'required|numeric'" :error-messages="errors.collect('goal')" name="goal"></v-text-field>
                        </v-card-text>
                        <v-card-text class="text-center">
                            <v-row align="center">
                                <v-col cols="12">
                                    <v-menu v-model="menu1" :close-on-content-click="false" max-width="290">
                                        <template v-slot:activator="{ on }">
                                            <v-text-field :value="computedDateFormatted" clearable label="Expiry Date of Campaign" readonly v-on="on"></v-text-field>
                                        </template>
                                        <v-date-picker v-model="date" @change="menu1 = false" :min="minDate"></v-date-picker>
                                    </v-menu>
                                </v-col>
                            </v-row>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn dark class="primary" rounded large @click.prevent="goStage1" :loading="isLoading">Go Stage 1</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn dark class="primary" rounded large @click.prevent="goStage3" :loading="isLoading">Next</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>


<script>
import moment from 'moment'
export default {
    data() {
        return {
            rules: {
                required: value => !!value || 'Required.',
                min: v => v.length === 4 || 'Pin must be 4 characters'
            },
            date: new Date().toISOString().substr(0,10),
            minDate: new Date().toISOString().substr(0, 10),
            menu1: false,
            modal: false,
            create: {
                goal: null,
                expiry: null
            },
            api: "http://localhost:8000/api/",
            isLoading: false
        }
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.isLoggedIn) {
                next();
            }else{
                next('/')
            }
        });
    },
    computed: {
        isLoggedIn(){
            return this.$store.getters.isLoggedIn
        },
        newCampaign(){
            return this.$store.getters.newCampaign
        },
        computedDateFormatted(){
            return this.date ? moment(this.date).format('dddd, MMM Do YYYY') : ''
        }
    },
    methods: {
        goStage1(){
            this.$router.push({name: 'CreateNew'})
        },
        goStage3(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid && this.date !== null) {
                   this.isLoading = true
                   const stored = localStorage.getItem('new_campaign')
                   if(stored){
                      let parsed = JSON.parse(stored)
                      parsed.goal = this.create.goal
                      parsed.expiry = moment(this.date).format('YYYY-MM-DD HH:mm:ss')
                      localStorage.setItem('new_campaign', JSON.stringify(parsed))
                   }else{
                    this.$router.push({name: 'CreateNew'})
                   }
                   this.$router.push({name: 'CreateNew3'})
                }
            })
        },
        getStoredData(){
            const data = localStorage.getItem('new_campaign')
            const stored = data ? JSON.parse(data) : null
            if(data){
                this.create.goal = stored.goal
                this.date = stored.expiry
            }
        }
    },
    created() {
       this.getStoredData()
    },
}
</script>