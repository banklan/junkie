<template>
    <div class="payment_gateway">
        <v-container>
            <v-row wrap>
                <v-col cols="4">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="7">
                    <v-card light elevation="6" class="my-5 pb-5">
                        <v-card-title class="justify-center mb-4 primary white--text">Donation Details</v-card-title>
                        <v-card-text align="start" class="mt-4 pt-3">
                            <table class="table table-condensed table-striped">
                                <tr>
                                    <th width="35%">Show Name:</th>
                                    <td>{{ backing.show_name ? 'Yes' : 'No' }}</td>
                                </tr>
                                <tr>
                                    <th>Name:</th>
                                    <td>{{ getAuthUser.fullname }}</td>
                                </tr>
                                <tr>
                                    <th>Email:</th>
                                    <td>{{ getAuthUser.email }}</td>
                                </tr>
                                <tr>
                                    <template v-if="!amountUpdateForm">
                                        <th>Amount To Donate(&#8358;):</th>
                                        <td><strong>{{ backing.amount / 100 | price }}</strong></td>
                                        <td><v-btn text small color="primary" @click="updateAmount"><v-icon small>edit</v-icon></v-btn></td>
                                    </template>
                                    <template v-else>
                                        <th class="mt-5">Amount To Donate(&#8358;):</th>
                                        <td>
                                            <v-text-field dense v-model="updtAmt" required v-validate="'required|numeric'" :error-messages="errors.collect('amount')" name="amount"></v-text-field>
                                        </td>
                                        <td class="d-flex">
                                            <v-btn text small color="pink darken--2" @click="amountUpdateForm = false">Cancel</v-btn>
                                            <v-btn small class="primary" @click="SaveUpdatedAmount">Update</v-btn>
                                        </td>
                                    </template>
                                </tr>
                            </table>
                        </v-card-text>
                       <v-card-actions class="justify-center">
                           <!-- <v-btn large class="primary" @click="openPaystack">Checkout</v-btn> -->
                            <paystack
                                :amount="backing.amount"
                                :email="getAuthUser.email"
                                :paystackkey="paystackkey"
                                :reference="getTrxRef"
                                :callback="callback"
                                :close="close"
                                :embed="false"
                                class="btn btn-primary"
                                >
                                Make Payment
                            </paystack>
                       </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
            <v-snackbar v-model="checkOutFail" :time="5000" top color="red darken-2 white--text">Payment failed. Please ensure your account was not debitted before retrying. Thank you. 
                <v-btn text color="white--text" @click="checkOutFail = false">Close</v-btn>
            </v-snackbar>
        </v-container>
    </div>
</template>


<script>
import paystack from 'vue-paystack';
export default {
    components: {
        paystack
    },
    data() {
        return {
            paystackkey: "pk_test_ff7d1752cae4dd879bab9f31890ae26f459d3742",
            amountUpdateForm: false,
            isLoading: false,
            api: "http://localhost:8000/api/",
            checkOutFail: false,
            updtAmt: 0
            // editAmount: parseInt(this.backing.amount) / 100
        }
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.authToken && vm.backing) {
                next();
            }else{
                next('/')
            }
        });
    },
    computed: {
        backing(){
            return this.$store.getters.backing
        },
        getAuthUser(){
            return this.$store.getters.getAuthUser
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
        campaign(){
            return this.$store.getters.getCampaign
        },
        getTrxRef(){
            return this.$store.getters.getTrxref
        },
        editAmount(){
            var amount = parseFloat(this.$store.getters.backing.amount / 100)
            return amount
        }
    },
    methods: {
        // payViaService(){
        //     this.payWithFlutterWave(this.paymentData)
        // },
        // redirectToGetway(){
        //     this.$validator.validateAll().then((isValid) => {
        //         if(isValid){
        //             this.generateTxRef()
        //             this.isLoading = true
        //             var amount = this.amount
        //             var currency = 'NGN'
        //             var redirect_url = 'http://127.0.0.1:8000/checkedout_successful'
        //             var payment_options = "card"

        //             this.$axios.post('https://api.flutterwave.com/v3/payments', {
        //                 amount: amount,
        //                 currency: currency,
        //                 redirect_url: redirect_url,
        //                 payment_options: payment_options,
        //                 customer: {
        //                     email: this.getAuthUser.email,
        //                     phonenumber: this.getAuthUser.phone_no,
        //                     name: this.getAuthUser.fullname
        //                 },
        //                 customizations:{
        //                     title: "Kolabo",
        //                     description: "Some Kolabo Description",
        //                     logo: "https://assets.piedpiper.com/logo.png"
        //                 },
        //                 tx_ref: this.getTrxRef
        //             })
        //             .then((res) => {
        //                 console.log(res.data)
        //             })
        //         }
        //     })
            
        // },
        updateAmount(){
            // this.backing.amount = this.updtAmt
            this.updtAmt = this.backing.amount / 100
            this.amountUpdateForm = true
        },
        SaveUpdatedAmount(){
            this.backing.amount = this.updtAmt * 100
            this.amountUpdateForm = false
        },
        generateTxRef(){
            this.$store.commit("genTrxRef")
        },
        callback: function(response){
            console.log(response)
            this.close()
            this.saveDonation(response)
        },
        close: function(){
            console.log("Payment closed")
        },
        saveDonation(res){
            if(res.status === 'success'){
                this.isLoading = true
                this.$axios.post(this.api + `post-donation/${this.campaign.id}/`, {
                    show_name: this.backing.show_name,
                    amount: this.backing.amount / 100,
                    comment: this.backing.comment,
                    trx_ref: this.getTrxRef,
                    trx_id: res.trans,
                    trx_msg: res.message
                }, this.config).then((res) => {
                    console.log(res.data)
                    this.isLoading = false
                    window.localStorage.removeItem('backing')
                    window.localStorage.removeItem('campaign_to_back')
                    window.localStorage.removeItem('trx-ref')
                    this.$router.push({name: 'CheckedOutSuccess'})
                }).catch(() => {
                    this.isLoading = false
                    this.checkOutFail = true
                })
            }
        }
    },
    mounted(){
        this.generateTxRef()
    }
}
</script>