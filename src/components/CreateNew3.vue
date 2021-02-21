<template>
    <div class="expiry">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12">
                    <div class="headline mb-5">Ok, just one more step to go (Step 3 of 3)</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="8">
                    <v-card light outlined min-height="200" class="px-6 py-4">
                        <v-card-title class="title justify-center mb-6 primary--text">
                            Tell us the titles and details of your campaign
                        </v-card-title>
                        <v-card-text align="start" class="mt-3">
                            <v-text-field label="Title of your campaign" hint="What is your campaign about?" v-model="create.title" required v-validate="'required|min:10|max:255'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                            <v-textarea label="Details" hint="Tell us the details" v-model="create.details" auto-grow rows="2" required v-validate="'required|min:20'" :error-messages="errors.collect('details')" name="details"></v-textarea>
                        </v-card-text>
                        <v-card-actions>
                            <v-btn class="primary" large dark @click="preview">Preview Your Campaign</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>


<script>

export default {
    data() {
        return {
            isLoading: false,
            create: {
                title: '',
                details: ''
            }
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
    },
    methods: {
        goStage2(){
            this.$router.push({name: 'CreateNew2'})
        },
        preview(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.isLoading = true
                    const stored = localStorage.getItem('new_campaign')
                    if(stored){
                        let parsed = JSON.parse(stored)
                        parsed.title = this.create.title
                        parsed.details = this.create.details
                        localStorage.setItem('new_campaign', JSON.stringify(parsed))
                    }else{
                        this.$router.push({name: 'CreateNew'})
                    }
                    this.$router.push({name: 'NewCampaignReview'})
                }
            })
        },
        getStoredData(){
            const stored = localStorage.getItem('new_campaign')
            if(stored){
                let parsed = JSON.parse(stored)
                this.create.title = parsed.title
                this.create.details = parsed.details
            }
        }
    },
    created() {
        this.getStoredData()
    },
}
</script>

<style scoped lang="scss">
    img{
        border-radius: 10px !important;
    }
</style>