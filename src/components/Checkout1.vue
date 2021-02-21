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
                        <v-card-title class="justify-center mb-4 primary white--text">Quickteller Payment Gateway</v-card-title>
                        <v-card-text align="start" class="mt-4 pt-3">
                            <v-text-field v-model="amount" label="Amount To Donate (In Naira)" hint="Please enter amount without comma" required v-validate="'required|numeric'" :error-messages="errors.collect('amount')" name="amount"></v-text-field>
                        </v-card-text>
                        <v-card-text align="">
                            <div class="title mb-5"> Enter your card details </div>
                            <v-text-field v-model="cardNo" :mask="mask" label="Credit Card No" :rules="[rules.required]" v-validate="'required|numeric|min:16|max:16'" :error-messages="errors.collect('card_no')" name="card_no"></v-text-field>
                            <v-row wrap>
                                <v-col cols="6">
                                    <v-text-field type="password" v-model="pin" label="Card Pin" :rules="[rules.required]" hint="Your 4-digits card Pin" v-validate="'required|numeric|min:4|max:4'" :error-messages="errors.collect('card_pin')" name="card_pin"></v-text-field>
                                </v-col>
                                <v-col cols="6">
                                    <v-text-field v-model="cvv" label="CVV Number" :rules="[rules.required]" hint="Your card security number"></v-text-field>
                                </v-col>
                            </v-row>
                            <v-dialog ref="dialog" v-model="modal" :return-value.sync="date" persistent max-width="350px">
                                <template v-slot:activator="{ on }">
                                    <v-text-field v-model="date" label="Expiry Date" readonly v-on="on" :rules="[rules.required]"></v-text-field>
                                </template>
                                <v-date-picker v-model="date" type="month" scrollable>
                                    <v-spacer></v-spacer>
                                    <v-btn text color="primary" @click="modal = false">Cancel</v-btn>
                                    <v-btn text color="primary" @click="$refs.dialog.save(date)">OK</v-btn>
                                </v-date-picker>
                            </v-dialog>
                        </v-card-text>
                        <v-card-actions class="mb-6 justify-center">
                            <v-btn large dark color="primary white--text" width="50%" @click.prevent="generateTrxRef" :loading="isLoading">Checkout</v-btn>
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
export default {
    data() {
        return {
            amount: null,
            rules: {
                required: value => !!value || 'Required.',
                min: v => v.length === 4 || 'Pin must be 4 characters'
            },
            mask: 'credit-card',
            cardNo: '0000000000000000',
            expiry: null,
            cvv: null,
            pin: null,
            date: new Date().toISOString().substr(0,7),
            modal: false,
            isLoading: false,
            api: "http://localhost:8000/api/",
            checkOutFail: false
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
    },
    methods: {
        redirectToGetway(){
            this.$validator.validateAll().then((isValid) => {
                if(isValid){
                    this.generateTxRef()
                    this.isLoading = true
                    this.$axios.post(this.api + `create-tx-ref/`, this.config)
                        .then((res) => {
                            console.log(res.data)
                        })
                }
            })
        },
        checkout(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    // console.log(this.campaign)
                    this.$store.dispatch("genTrxRef");
                    this.isLoading = true
                    this.$axios.post(this.api + `post-donation/${this.campaign.id}/`, {
                        // project: this.campaign,
                        show_name: this.backing.show_name,
                        amount: this.amount,
                        comment: this.backing.comment
                    }, this.config).then((res) => {
                        console.log(res.data)
                         this.isLoading = false
                         window.localStorage.removeItem('backing')
                         window.localStorage.removeItem('campaign_to_back')
                        this.$router.push({name: 'CheckedOutSuccess'})
                    }).catch(() => {
                        this.isLoading = false
                        this.checkOutFail = true
                    })
                }
            })    
        }
    },
}
</script>