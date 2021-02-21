<template>
    <div class="request_withdrawal">
        <v-container>
            <v-row wrap align="center" justify="center">
                <v-col cols="12" md="8">
                    <template v-if="cantRequestWithrawal">
                        <v-alert type="error" align="start" class="mt-5">
                            {{ cantWithrawError }}
                        </v-alert>
                    </template>
                    <template v-else>
                        <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                        <template v-else>
                            <template v-if="campaign">
                                <v-card light shaped elevation="6" min-height="350">
                                    <v-card-title class="title primary white--text justify-center">Request Withdrawal</v-card-title>
                                    <v-card-text class="mt-3" align="start">
                                        <v-alert type="info" class="mb-3">
                                            On this page, you can request for your donated fund withdrawal.
                                        </v-alert>
                                        <table v-if="campaign" class="table table-condensed table-stripe table-hover table-bordered">
                                            <thead></thead>
                                            <tbody>
                                                <tr>
                                                    <th width="35%">Campaign Title</th>
                                                    <td class="font-weight-bold">{{ campaign.title }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Published Date</th>
                                                    <td>{{ campaign.created }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Expiry Date</th>
                                                    <td>{{ campaign.expiry }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Goal(&#8358;):</th>
                                                    <td class="font-weight-bold">{{ campaign.goal | price }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Total Donation(&#8358;):</th>
                                                    <td class="font-weight-bold">{{ campaign.total_donations | price }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Percentage Raised:</th>
                                                    <td class="font-weight-bold">{{ campaign.percent_raised }}%</td>
                                                </tr>
                                                <tr>
                                                <th>Withdrawable Fund(&#8358;):</th>
                                                <td class="font-weight-bold primary--text">{{ withdrawable | price }}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <v-alert type="info" class="caption">
                                            Please note that Charges of 11% are applied to the total donated fund at withdrawal. By clicking the Request Withdrawal button below, you have agreed to the terms and policy guiding withdrawal of donated funds on kolabo. 
                                        </v-alert>
                                    </v-card-text>
                                    <v-card-actions class="justify-center pb-5">
                                        <v-btn class="primary" large :loading="requesting" @click="sendRequest">Request Withdrawal</v-btn>
                                    </v-card-actions>
                                </v-card>
                            </template>
                            <template v-else>
                                <template v-if="invalidCampaign">
                                    <v-alert border="left" type="error">
                                        You have selected an invalid campaign.
                                    </v-alert>
                                </template>
                            </template>
                        </template>
                    </template>
                </v-col>
            </v-row>
            <v-snackbar v-model="requestFailed" :time="5000" top color="red darken-2 white--text">Your request cannot be completed now. Please try again. 
                <v-btn text color="white--text" @click="requestFailed = false">Close</v-btn>
            </v-snackbar>
        </v-container>
    </div>
</template>

<script>
export default {
    data() {
        return {
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            // partWithdrawal: false,
            // partAmount: 0,
            amountToWithdraw: 0,
            isLoading: false,
            campaign: null,
            api: "http://localhost:8000/api/",
            invalidCampaign: false,
            requesting: false,
            cantRequestWithrawal: false,
            cantWithrawError: '',
            requestFailed: false
        }
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.authToken) {
                next();
            }else{
                next('/')
            }
        });
    },
    computed: {
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
        fullHeader() {
            let conf = {
                headers: {
                    Authorization: "Token " + this.authToken,
                    "Content-Type": "multipart/form-data",
                },
            };
            return conf;
        },
        getAuth(){
            return this.$store.getters.getAuthUser
        },
        withdrawable(){
            let amount = this.campaign.total_donations
            let charges = amount * 0.11
            let withdrawable = amount - charges
            return withdrawable
        }
    },
    methods: {
        getCampaign(){
            this.isLoading = true
            this.$axios.get(this.api + `projects_by_slug/${this.slug}/`).then((res) =>{
                console.log(res.data)
                this.isLoading = false
                let rez = res.data
                let author = rez.author.id
                let auth = this.getAuth.id

                if(author !== auth){
                    this.cantRequestWithrawal = true
                    this.cantWithrawError = 'You are not authorized to request withdrawal from this campaign.'
                }else if(rez.to_expire > 0){
                    this.cantRequestWithrawal = true
                    this.cantWithrawError = 'You cannot request withdrawal from this campaign as request can only be made when your campaign has expired.'
                }else if(rez.total_donations < 5000){//total donation must be greater than 5k
                    this.cantRequestWithrawal = true
                    this.cantWithrawError = 'You cannot request withdrawal as the donated fund is too small.'
                }else{
                    // this.checkIfRequestExist(rez)
                    this.checkAccountLinked(rez)
                }
            }).catch(() =>{
                this.isLoading = false
                this.invalidCampaign = true
            })
        },
        checkAccountLinked(rez){
            this.$axios.get(this.api + 'check-linked-account/', this.config).then((res) => {
                if(res.data.status === 404){
                    // console.log(res.data.status)
                    this.cantRequestWithrawal = true
                    this.cantWithrawError = 'You cannot request withdrawal until you provide the details of your bank account. Please go to your Profile page and link your bank account.'
                }else{
                    // check if request exist for this project
                    this.$axios.get(this.api + `check_withdrawal_request/${rez.id}/`, this.config).then((res) => {
                        if(res.data.status == 404){
                            this.campaign = rez
                            this.amountToWithdraw = this.withdrawable
                        }else{
                            this.cantRequestWithrawal = true
                            this.cantWithrawError = 'Duplicate request. You have already lodged a withdrawal request for this campaign.'
                        }
                    })
                }
            }).catch(() =>{
                this.cantRequestWithrawal = true
                this.cantWithrawError = 'You cannot request withdrawal until you provide the details of your bank account. Please go to your Profile page and link your bank account.'
            })
        },
        sendRequest(){
            this.requesting = true
            this.$axios.post(this.api + `withdrawal_request/${this.id}/`, {
                amount: parseFloat(this.amountToWithdraw)
            }, this.config).then((res) => {
                this.requesting = false
                this.requestSuccess = true
                this.$router.push({name: 'WithdrawReqSuccess'})
                console.log(res.data)
            }).catch(() => {
                this.requesting = false
                this.requestFailed = true
            })
        }
    },
    created() {
        this.getCampaign()
    },
}
</script>