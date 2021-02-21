<template>
    <div class="edit_campaign">
        <v-container>
            <v-row wrap justify="center" class="mt-3">
                <v-col cols="3" md="2">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back </v-btn>
                </v-col>
                <v-col cols="9" md="10">
                    <div class="title font-weight-bold">Manage Campaign</div>
                </v-col>
            </v-row>
            <v-row wrap justify="start" align="start" class="mt-3">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                <template v-else>
                    <v-col cols="12">
                        <template v-if="invalidCampaign">
                            <v-alert border="left" type="error">
                                You have selected an invalid campaign.
                            </v-alert>
                        </template>
                        <template v-else>
                            <!-- <v-card light> -->
                                <v-tabs v-model="tab" background-color="primary" dark>
                                    <v-tab>Dashboard</v-tab>
                                    <v-tab>Edit Campaign</v-tab>
                                    <v-tab>Campaign Image</v-tab>
                                    <v-tab>Modify Expiry</v-tab>
                                    <v-tab>Updates</v-tab>
                                    <v-tab>Success Story</v-tab>
                                </v-tabs>
                                <v-tabs-items v-model="tab">
                                    <v-tab-item>
                                        <v-card flat min-height="200">
                                            <v-row align="start" class="px-5">
                                                <div class="title mt-4 ml-8">Dashboard</div>
                                            </v-row>
                                            <v-row align="start" justify="start">
                                                <v-col cols="12" md="6">
                                                    <v-card-text align="start" justify="start">
                                                        <table class="table table-bordered table-hover table-striped">
                                                           <thead></thead>
                                                           <tbody>
                                                               <tr height="35" class="subtitle-1">
                                                                    <th align="start">Published</th>
                                                                    <td>{{ campaign.created }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Views</th>
                                                                    <td>{{ campaign.view_count }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Goal</th>
                                                                    <td><strong>&#8358;{{ campaign.goal | price }}</strong></td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Amount Raised</th>
                                                                    <td><strong>&#8358;{{ campaign.total_donations | price }}</strong></td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Percent Raised</th>
                                                                    <td>{{ campaign.percent_raised }}%</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">No of Backers</th>
                                                                    <td>{{ campaign.donations.length }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">No of Followers</th>
                                                                    <td>{{ campaign.followers.length }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Expiry</th>
                                                                    <td>{{ campaign.expiry }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Goal Status</th>
                                                                    <td>{{ campaign.status }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Withdrawal Request</th>
                                                                    <td>{{ withdrawalReqStatus }}</td>
                                                                </tr>
                                                                <tr height="35" class="subtitle-1">
                                                                    <th align="start">Fund Status</th>
                                                                    <td v-if="campaign.paid == false">Not Yet Withdrawn</td>
                                                                    <td v-if="campaign.paid == true">Fund Withdrawn</td>
                                                                </tr>
                                                           </tbody>
                                                        </table>
                                                        <div class="mt-3">
                                                            <template v-if="campaign.paid">
                                                                <v-alert type="info">
                                                                    The fund donated for this campaign has been disbursed to your account and campaign marked as Completed. If you haven't received the payment, please contact us.
                                                                </v-alert>
                                                            </template>
                                                            <template v-else>
                                                               <v-alert type="info" class="mt-5">
                                                                  Please note that you can only request withdrawal when your campaign has expired.
                                                               </v-alert>
                                                               <table v-if="campaign.to_expire < 0" class="table table-condensed mt-5 pa-5">
                                                                  <tr height="30" v-if="withdrawalReqStatus == 'No Request'">
                                                                     <th class="pt-6">Request Withdrawal?</th>
                                                                     <td class="pt-5"><v-btn class="primary" @click="WithdrawFund">Withdraw</v-btn></td>
                                                                  </tr>
                                                               </table>
                                                            </template>
                                                        </div>
                                                    </v-card-text>
                                                </v-col>
                                            </v-row>
                                        </v-card>
                                    </v-tab-item>
                                    <v-tab-item>
                                        <v-card flat min-height="200">
                                            <v-row align="start" class="px-5">
                                                <div class="title mt-4 ml-5">Edit Campaign</div>
                                            </v-row>
                                            <v-row align="start" justify="start">
                                                <v-col cols="12" md="8">
                                                    <template v-if="showEdit">
                                                        <template v-if="withdrawalReqStatus == 'No Request'">
                                                            <template v-if="!edit">
                                                                <v-card-title class="ml-3 title">{{ campaign.title | capFirstLetter }}</v-card-title>
                                                                <v-card-text align="start" class="ml-3 subtitle-1">{{ campaign.details | capFirstLetter }}</v-card-text>
                                                                <v-card-actions class="justify-center">
                                                                    <v-btn outlined dark color="primary" @click="edit = true"><v-icon left>edit</v-icon></v-btn>
                                                                </v-card-actions>
                                                            </template>
                                                            <template v-else>
                                                                <v-card-text align="start" class="ml-3">
                                                                    <v-text-field label="Title" v-model="campaign.title" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                                                                    <v-textarea label="Details" v-model="campaign.details" required v-validate="'required|min:30|max:3000'" :error-messages="errors.collect('details')" name="details"></v-textarea>
                                                                </v-card-text>
                                                                <v-card-actions class="justify-center pb-7 mt-4 ml-3">
                                                                    <v-btn dark class="primary" large width="50%" @click="updateCampaign" :loading="isUpdating">Save</v-btn>
                                                                </v-card-actions>
                                                            </template>
                                                        </template>
                                                        <template v-else>
                                                            <div class="subtitle-1 primary--text ml-5" align="start">
                                                                You cannot modify the contents of this campaign since you have requested for fund withdrawal. Thank You.
                                                            </div>
                                                        </template>
                                                    </template>
                                                </v-col>
                                            </v-row>
                                        </v-card>
                                    </v-tab-item>
                                    <v-tab-item>
                                        <v-card flat min-height="200">
                                            <v-row align="start" class="px-5">
                                                <div class="title mt-4 ml-5">Change Campaign Image</div>
                                            </v-row>
                                            <v-row align="start" justify="start">
                                                <v-col cols="12" md="8">
                                                    <div class="ml-5 mt-4" v-if="withdrawalReqStatus == 'No Request'">
                                                        <template v-if="!previewImg">
                                                            <v-img :src="campaign.image" aspect-ratio="1" height="380" transition="scale-transition"></v-img>
                                                            <v-card-text align="center" class="mt-3">
                                                                <v-btn large dark color="primary" class="mb-5 ml-5" @click="openUpload">Choose New Picture</v-btn>
                                                                <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                                                            </v-card-text>
                                                        </template>
                                                        <template v-else>
                                                            <template v-if="!imageUpdating">
                                                                <v-img :src="previewImgUrl" height="360" contain alt="Preview image" aspect-ratio="1"></v-img>
                                                                <v-card-text class="title justify-center mt-1">Preview</v-card-text>
                                                                <v-card-actions class="mt-1 pb-6 justify-center">
                                                                    <v-btn text large color="red darken-2" @click="cancelUpload">Cancel</v-btn>
                                                                    <v-btn dark x-large color="primary" :loading="loading" @click="updateImg">Update Image</v-btn>
                                                                </v-card-actions>
                                                            </template>
                                                            <template v-else>
                                                                <v-progress-circular indeterminate color="primary lighten-2" :width="10" :size="70" justify="center" class="mx-auto mt-5"></v-progress-circular>
                                                            </template>
                                                        </template>
                                                    </div>
                                                    <template v-else>
                                                        <div class="subtitle-1 primary--text ml-5" align="start">
                                                            You cannot modify the contents of this campaign since you have requested for fund withdrawal. Thank You.
                                                        </div>
                                                    </template>
                                                </v-col>
                                            </v-row>
                                        </v-card>
                                    </v-tab-item>
                                    <v-tab-item>
                                        <v-card flat min-height="200">
                                            <v-row align="start" class="px-5">
                                                <div class="title mt-4 ml-5">Update Expiry</div>
                                            </v-row>
                                            <v-row align="start" justify="start">
                                                <v-col cols="12" md="8">
                                                    <template v-if="withdrawalReqStatus == 'No Request'">
                                                        <v-alert type="info" border="left" align="start">
                                                            Please note that you can only update your campaign expiry date once in the lifecycle of that campaign.
                                                        </v-alert>
                                                        <v-card-text class="subtitle-1" align="start">
                                                            Expiry Date: {{ campaign.expiry }}
                                                        </v-card-text>
                                                        <template v-if="campaign.can_update_expiry">
                                                            <v-card-text class="text-center">
                                                                <v-row align="center">
                                                                    <v-col cols="12" md="7">
                                                                        <v-menu v-model="menu1" :close-on-content-click="false" max-width="290">
                                                                            <template v-slot:activator="{ on }">
                                                                                <v-text-field :value="computedDateFormatted" clearable label="Choose a new expiry date" readonly v-on="on"></v-text-field>
                                                                            </template>
                                                                            <v-date-picker v-model="date" @change="menu1 = false" :min="minDate"></v-date-picker>
                                                                        </v-menu>
                                                                    </v-col>
                                                                </v-row>
                                                            </v-card-text>
                                                            <v-card-actions align="left" class="mt-3 pb-6 ml-2">
                                                                <v-btn dark color="primary" @click="updateExpiry" :loading="loading">Update Expiry</v-btn>
                                                            </v-card-actions>
                                                        </template>
                                                    </template>
                                                    <template v-else>
                                                        <div class="subtitle-1 primary--text darken-4 ml-5" align="start">
                                                            You cannot modify the contents of this campaign since you have requested for fund withdrawal. Thank You.
                                                        </div>
                                                    </template>
                                                </v-col>
                                            </v-row>
                                        </v-card>
                                    </v-tab-item>
                                    <v-tab-item>
                                        <v-card flat min-height="200">
                                            <v-row justify="space-between" class="mt-3">
                                                <v-col cols="3">
                                                    <div class="title ml-4" align="start">Updates</div>
                                                </v-col>
                                                <v-col cols="5" v-if="!addUpdate">
                                                    <v-btn dark color="primary" @click="addUpdate = true"><v-icon left>add</v-icon>New Update</v-btn>
                                                </v-col>
                                            </v-row>
                                            <v-row wrap justify="start">
                                                <v-col cols="12" md="8">
                                                    <template v-if="addUpdate">
                                                        <add-update :campaign="campaign"></add-update>
                                                    </template>
                                                    <template v-else>
                                                        <div v-for="(update, i) in campaign.updates" :key="i">
                                                            <my-update :update="update" :index="i"></my-update>
                                                        </div>
                                                    </template>
                                                </v-col>
                                            </v-row>
                                        </v-card>
                                    </v-tab-item>
                                    <v-tab-item>
                                        <v-card flat min-height="200">
                                            <v-row wrap justify="start" class="pa-2">
                                                <v-col cols="12" md="8">
                                                    <v-alert type="info" border="left" class="ml-3">
                                                        Success Story is an opportunity to share the testimonies of your successful fundraising journey with your backers.
                                                        Make it concise and short. You can only write one for a campaign.
                                                    </v-alert>
                                                </v-col>
                                            </v-row>
                                            <my-success-story :campaign="campaign"></my-success-story>
                                        </v-card>
                                    </v-tab-item>
                                </v-tabs-items>
                            <!-- </v-card> -->
                        </template>
                    </v-col>
                </template>
            </v-row>
                
        </v-container>
        <v-snackbar v-model="updatedSuccess" :time="3500" top color="green darken-2 white--text">Your campaign has been updated successfully. 
            <v-btn text color="white--text" @click="updatedSuccess = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="imageUploadSuccess" :time="3500" top color="green darken-2 white--text">Your campaign image has been updated. 
            <v-btn text color="white--text" @click="imageUploadSuccess = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="imageUploadFail" :time="6000" top color="red darken-2 white--text">The update failed. Please try again. 
            <v-btn text color="white--text" @click="imageUploadFail = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="expiryUpdated" :time="3000" top color="green darken-2 white--text">Your campaign expiry date has been updated. 
            <v-btn text color="white--text" @click="expiryUpdated = false">Close</v-btn>
        </v-snackbar>
    </div>
</template>

<script>
import moment from 'moment'
import EventBus from '../bus'

export default {
    data() {
        return {
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            tab: null,
            campaign: null,
            api: "http://localhost:8000/api/",
            invalidCampaign: false,
            showEdit: false,
            isLoading: false,
            modify: {
                title: '',
                details: '',
            },
            isUpdating: false,
            updatedSuccess: false,
            prevImg: false,
            image: null,
            previewImgUrl: '',
            previewImg: false,
            loading: false,
            imageUploadSuccess: false,
            imageUpdating: false,
            imageUploadFail: false,
            menu1: false,
            date: new Date().toISOString().substr(0,10),
            minDate: new Date().toISOString().substr(0, 10),
            expiryUpdated: false,
            edit: false,
            addUpdate: false,
            updateEditForm: false,
            withdrawalReqStatus: ''
        }
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
        campaignToModify(){
            return this.$store.getters.getCampaignToModify
        },
        computedDateFormatted(){
            return this.date ? moment(this.date).format('dddd, MMM Do YYYY') : ''
        }
    },
    methods: {
        getCampaign(){
            this.isLoading = true
            this.$axios.get(this.api + `projects/${this.id}/`).then((res) =>{
                console.log(res.data)
                this.isLoading = false
                let author = res.data.author.id
                let auth = this.getAuth.id
                if(author == auth){
                    // this.showDash = true
                    this.showEdit = true
                    this.campaign = res.data
                }
                //check if withdrawal request has been made
                this.checkWithdrawalRequest(res.data)
            }).catch(() =>{
                this.isLoading = false
                this.invalidCampaign = true
            })
        },
        checkWithdrawalRequest(campaign){
            this.$axios.get(this.api + `check_withdrawal_request/${campaign.id}/`, this.config).then((res) => {
                if(res.data.status == 404){
                    this.withdrawalReqStatus = 'No Request'
                }else{
                    console.log(res.data)
                    if(res.data.is_approved == true){
                        this.withdrawalReqStatus = 'Request Approved'
                    }else{
                        this.withdrawalReqStatus = 'Request Pending'
                    }
                }
            })
                     
        },
        updateCampaign(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.isUpdating = true
                    this.$axios.patch(this.api + `update-my-project-details/${this.campaign.id}/`, {
                        title: this.campaign.title,
                        details: this.campaign.details
                    }, this.config).then(() => {
                        this.updatedSuccess = true
                        this.edit = false
                    })
                }
            })
        },
        openUpload(){
            this.$refs.image.click()
        },
        pickImg(e){
            const file = e.target.files[0]
            this.image = file
            this.previewImg = true
            this.previewImgUrl = URL.createObjectURL(file)
        },
        cancelUpload(){
            this.previewImgUrl = '';
            this.previewImg = false;
        },
        updateImg(){
            if(this.image !== null){
                this.loading = true
                let form = new FormData();
                form.append('image', this.image)

                this.$axios.put(this.api + `create-project-image/${this.campaign.id}/`, form, this.fullHeader).then((res) => {
                    console.log(res.data)
                    this.campaign.image = res.data.image
                    this.imageUploadSuccess = true
                    this.imageUpdating = true
                    this.previewImg = false
                }).catch(() => {
                    this.loading = false
                    this.imageUploadFail = true
                })
            }
        },
        updateExpiry(){
            if(this.date !== null){
                this.loading = true
                let expiry = moment(this.date).format('YYYY-MM-DD HH:mm:ss')
                this.$axios.patch(this.api + `update-expiry-date/${this.campaign.id}/`, {
                    expiry: expiry
                }, this.config).then((res) => {
                    console.log(res.data)
                    this.loading = false
                    this.expiryUpdated = true
                    setTimeout(() => {
                        this.$router.push({name: 'MyProfile'})
                    }, 3000);
                })
            }
        },
        editUpdate(updt){
            this.updateToModify = updt
            this.updateEditForm = true
        },
        WithdrawFund(){
            if(this.campaign.to_expire < 0){
                this.$router.push({name: 'RequestWithdrawal', params: {campaign: this.id, slug: this.slug}})
            }
        }
    },
    created() {
        this.getCampaign()
    },
    mounted(){
        EventBus.$on('remove-del', (index) => {
            this.campaign.updates.splice(index, 1)
        })

        EventBus.$on('update-added', () => {
            this.addUpdate = false
        })

        EventBus.$on('clear-form', (payload) => {
            this.addUpdate = false
            this.campaign.updates.unshift(payload)
        })
    }
}
</script>


<style lang="scss" scoped>
    .v-alert{
        line-height: 1.8 !important;
    }
</style>