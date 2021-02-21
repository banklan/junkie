<template>
    <div class="review">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12">
                    <div class="headline mb-5">Review Your Campaign Details</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="8">
                    <v-card light flat min-height="200" class="px-6 py-4">
                        <v-card-text>
                            <table class="table table-hover table-striped table-bordered table-responsive-sm" v-if="create">
                                <tr align="left">
                                    <th width="25%">Category: </th>
                                    <td class="">{{ create.category.name }}</td>
                                </tr>
                                <tr align="left" height="40">
                                    <th>Beneficiacy: </th>
                                    <td>{{ create.beneficiary }}</td>
                                </tr>
                                <v-btn small dark class="primary white--text my-3" :to="{name: 'CreateNew'}"><v-icon small left>edit</v-icon>Stage 1</v-btn>

                                <tr align="left" height="40">
                                    <th>Goal: </th>
                                    <td>&#8358;{{ parseInt(create.goal) | price }}</td>
                                </tr>
                                <tr align="left" height="40">
                                    <th>Expiry Date: </th>
                                    <td>{{ expiry }}</td>
                                </tr>
                                <v-btn small dark class="primary white--text my-3" :to="{name: 'CreateNew2'}"><v-icon small left>edit</v-icon> Stage 2</v-btn>
                                <tr align="left" height="40">
                                    <th>Title: </th>
                                    <td>{{ create.title }}</td>
                                </tr>
                                <tr align="left" min-height="40">
                                    <th>Details: </th>
                                    <td>{{ create.details }}</td>
                                </tr>
                                <v-btn small dark class="primary white--text my-3" :to="{name: 'CreateNew3'}"><v-icon small left>edit</v-icon> Stage 3</v-btn>
                            </table>
                        </v-card-text>
                        <v-card-actions class="justify-center">
                            <v-btn class="primary" large dark :to="{name: 'CreateAddImage'}">Upload Campaign Image</v-btn>
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
            isLoading: false,
            create: {},
            campaignSaved: false,
            api: "http://localhost:8000/api/",
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
        expiry(){
            return moment(this.create.expiry).format('dddd, Do MMMM, YYYY')
        },
        authToken() {
            return this.$store.getters.getToken;
        },
        config() {
            let conf = {
                headers: {
                    Authorization: "Token " + this.authToken,
                },
            };
            return conf;
        },
    },
    methods: {
        getStoredCampaign(){
            const stored = localStorage.getItem('new_campaign')
            if(stored){
                let parsed = JSON.parse(stored)
                this.create = parsed
            }
        },
    },
    created() {
        this.getStoredCampaign()
    },
}
</script>

<style scoped lang="scss">
   .v-data-table{
       font-size: 16px;
   }
</style>