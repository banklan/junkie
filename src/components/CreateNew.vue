<template>
    <div class="checked_out">
        <v-container>
            <v-row wrap>
                <v-col cols="4">
                    <v-btn rounded color="secondary" dark elevation="3" left to="/"><v-icon left>arrow_left</v-icon> Back To Home</v-btn>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12">
                    <div class="headline mb-5">Create new campaign (Step 1 of 3)</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="9">
                    <v-card light outlined min-height="200" class="px-6 py-4">
                        <v-card-title class="title justify-center mb-4 primary--text">
                            Choose the category and tell us the beneficiary of the proceeds of the campaign.
                        </v-card-title>
                        <v-card-text align="start">
                            <v-row wrap justify="start">
                                <v-col cols="12" md="6">
                                    <v-select label="Category" v-model="create.category" :items="categories" item-text="name" return-object required persistent-hint v-validate="'required'" :error-messages="errors.collect('category')" name="category"></v-select>
                                </v-col>
                            </v-row>
                            <v-text-field label="Beneficiary" hint="Name of Beneficiary (Just type 'self' if you are the beneficiary)" v-model="create.beneficiary" required v-validate="'required|max:100'" :error-messages="errors.collect('beneficiary')" name="beneficiary"></v-text-field>
                        </v-card-text>
                        <v-card-actions align="end">
                            <div class="flex-grow-1"></div>
                            <v-btn dark class="primary" rounded large @click.prevent="goStage2" :loading="isLoading">Next</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>


<script>
import EventBus from '../bus'
export default {
    data() {
        return {
            create: {
                beneficiary: '',
                category: null
            },
            categories: [],
            api: "http://localhost:8000/api/",
            isLoading: false
        }
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.isLoggedIn) {
                next();
            }else{
                vm.$store.commit("redirect_onlogin", '/create_new');
                next('/login')
            }
        });
    },
    computed: {
        authToken() {
            return this.$store.getters.getToken;
        },
        isLoggedIn(){
            return this.$store.getters.isLoggedIn
        },
        newCampaign(){
            return this.$store.getters.newCampaign
        }
    },
    methods: {
        getCategories(){
            this.$axios.get(this.api + 'categories/').then((res) => {
                this.categories = res.data
                // console.log(res.data)
            })
        },
        goStage2(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                   this.isLoading = true
                   const stored = localStorage.getItem('new_campaign')
                   if(stored){
                      const parsed = JSON.parse(stored)
                      parsed.category = this.create.category
                      parsed.beneficiary = this.create.beneficiary
                      localStorage.setItem('new_campaign', JSON.stringify(parsed))
                   }else{
                       localStorage.setItem('new_campaign', JSON.stringify(this.create))
                   }
                   this.$router.push({name: 'CreateNew2'})
                }
            })
        },
        getStoredData(){
            const data = localStorage.getItem('new_campaign')
            const stored = data ? JSON.parse(data) : null
            if(stored){
                this.create.beneficiary = stored.beneficiary
                this.create.category = stored.category
            }
        },
        mustLogIn(){
            EventBus.$emit('login-create')
        }
    },
    created() {
        this.getCategories()
        this.getStoredData()
    },
}
</script>