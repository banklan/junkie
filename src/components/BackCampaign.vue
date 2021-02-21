<template>
    <div class="back_campaign">
        <v-container>
            <v-row>
                <v-col cols="4" md="3">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
                </v-col>
                <v-col cols="8" md="7">
                    <div class="headline font-weight-medium"> Back campaign Page</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center" align="center" class="mt-7">
                <v-col cols="12" md="8">
                   <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                   <template v-else>
                       <template v-if="!campaign">
                           <v-alert border="left" type="warning">You have not selected a valid campaign to back.</v-alert>
                       </template>
                       <template v-else>
                            <v-card elevation="6" min-height="250" light>
                                <v-card-text class="ml-5 pt-5">
                                    <v-simple-table fixed-header min-height="150px" v-if="campaign" class="subtitle-1">
                                        <template v-slot:default>
                                            <tr align="left" height="40">
                                                <th width="20%">Campaign</th>
                                                <td class="primary--text">{{ campaign.title }}</td>
                                            </tr>
                                            <tr align="left" height="40">
                                                <th>Organizer: </th>
                                                <td>{{ campaign.author.fullname }}</td>
                                            </tr>
                                            <tr align="left" height="40" class="font-weight-bold">
                                                <th>Goal: </th>
                                                <td class="secondary--text darken-2">&#8358;{{ parseInt(campaign.goal) | price }}</td>
                                            </tr>
                                            <tr align="left" height="40" class="font-weight-bold">
                                                <th>Total Donations:</th>
                                                <td>&#8358;{{ parseInt(campaign.total_donations) | price }} ({{ campaign.percent_raised }}% of goal)</td>
                                            </tr>
                                            <tr align="left" height="40">
                                                <th>Published: </th>
                                                <td>{{ campaign.created }}</td>
                                            </tr>
                                            <tr align="left" height="40">
                                                <th>Expiry: </th>
                                                <td>{{ campaign.to_expire }} days</td>
                                            </tr>
                                        </template>
                                    </v-simple-table>
                                </v-card-text>
                            </v-card>
                            <v-card elevation="6" min-height="250" light class="mt-4 pb-5">
                                <v-card-text class="mx-5 mt-5">
                                    <div class="subtitle-1 pt-2 mb-n2" align="start">To show your donation as anonymous, click to leave the box unchecked. </div>
                                    <v-checkbox v-model="back.show_name" label="Show my Details?"></v-checkbox>
                                    <template v-if="back.show_name">
                                        <div class="subtitle-2 mt-n3" align="start">Your identity will show on your donation</div>
                                    </template>
                                    <template v-else>
                                        <div class="subtitle-2 mt-n3" align="start">Your identity will be hidden and shown as anonymous on your donation</div>
                                    </template>
                                    <div class="mt-8 pr-5">
                                        <div class="subtitle-1 mb-3" align="start">It's not all about the cash donations. Drop a short message for the campaigner showing you care.</div>
                                        <v-textarea auto-grow rows="2" v-model="back.comment" label="Message" placeholder="Message" v-validate="'required|min:5|max:150'" :counter="150" :error-messages="errors.collect('comment')" name="comment"></v-textarea>
                                    </div>
                                </v-card-text>
                                <v-card-text>
                                    <div class="title">How much are you donating (Naira)?</div>
                                    <v-row justify="center">
                                        <v-col cols="12" md="8">
                                            <v-text-field v-model.number="back.amount" placeholder="Amount" hint="No commas & period, just the figure e.g 50000 for fifty thousand naira" required v-validate="'required|numeric'" :error-messages="errors.collect('amount')" name="amount"></v-text-field>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions class="justify-center mb-4">
                                    <v-btn text class="red--text mr-3">Cancel</v-btn>
                                    <v-btn large color="primary" width="30%" @click.prevent="proceedToCheckOut">Proceed To Checkout</v-btn>
                                </v-card-actions>
                            </v-card>
                        </template>
                    </template>
                </v-col>
            </v-row>
            <v-snackbar v-model="minDonationAmttFail" :time="7000" top color="red darken-2 white--text">The minimum amount you can donate is N100. Please enter an amount greater than N100. 
                <v-btn text color="white--text" @click="minDonationAmttFail = false">Close</v-btn>
            </v-snackbar>
        </v-container>
    </div>
</template>


<script>
export default{
    data() {
        return {
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            api: "http://localhost:8000/api/",
            user: null,
            isLoading: false,
            back: {
                show_name: true,
                comment: '',
                amount: null
            },
            minDonationAmttFail: false
        }
    },
    computed: {
        campaign(){
            return this.$store.getters.getCampaign
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
        sendMessage(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.isLoading = true
                    this.$store.commit("donation_data", this.back);
                    this.$router.push({name: 'Checkout'})
                    this.isLoading = false
                }
            })
        },
        proceedToCheckOut(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    if(parseInt(this.back.amount) > 99){
                        this.isLoading = true
                        this.back.amount = this.back.amount * 100
                        this.$store.commit("donation_data", this.back);
                        this.$router.push({name: 'Checkout'})
                        this.isLoading = false
                    }else{
                        this.minDonationAmttFail = true
                    }
                }
            })
        }
    },
}
</script>


<style scoped>
    .comment_span{
        margin-top: 85px !important;
    }
</style>