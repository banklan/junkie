<template>
    <div class="edit_campaign">
        <v-container>
            <v-row wrap justify="center" class="mt-3">
                <v-col cols="4" md="3">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back </v-btn>
                </v-col>
                <v-col cols="8" md="9">
                    <div class="title font-weight-bold">Manage Campaign</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center" class="mt-3">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                <template v-else>
                    <v-col cols="12" md="4">
                        <v-card light flat min-height="350" elevation="6" class="mt-6">

                        </v-card>
                    </v-col>  
                    <v-col cols="12" md="8">
                        <template v-if="invalidCampaign">
                            <v-alert border="left" type="error">
                                You have selected an invalid campaign.
                            </v-alert>
                        </template>
                        <template v-else>
                            <template v-if="showEdit">
                                <v-card light flat elevation="6" min-height="400" class="mt-6 mb-6">
                                    <v-card-title class="primary white--text justify-center mb-6">Modify Campaign</v-card-title>
                                    <v-card-text align="start" class="pt-5">
                                        <v-text-field label="Title" v-model="campaign.title" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                                        <v-textarea label="Details" v-model="campaign.details" required v-validate="'required|min:30|max:3000'" :error-messages="errors.collect('details')" name="details"></v-textarea>
                                    </v-card-text>
                                    <v-card-actions class="justify-center pb-7 mt-3">
                                        <v-btn dark class="primary" large width="50%" @click="updateCampaign" :loading="isUpdating">Save</v-btn>
                                    </v-card-actions>
                                </v-card>

                                <v-card light flat elevation="6" min-height="400" class="mt-4 mb-6">
                                    <v-card-title class="primary white--text justify-center">
                                        Change Campaign Picture
                                    </v-card-title>
                                    <template v-if="!previewImg">
                                        <v-img :src="campaign.image" aspect-ratio="1" height="380" transition="scale-transition"></v-img>
                                        <v-card-text align="start" class="mt-3">
                                            <v-btn large dark color="primary" class="mb-5 ml-5" @click="openUpload">Choose New Picture</v-btn>
                                            <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                                        </v-card-text>
                                    </template>
                                    <template v-else>
                                        <template v-if="!imageUpdating">
                                            <v-img :src="previewImgUrl" height="380" contain alt="Preview image" aspect-ratio="1"></v-img>
                                            <v-card-text class="title justify-center mt-3 mb-3">Previewed Image</v-card-text>
                                            <v-card-actions class="mt-4 pb-6 justify-center">
                                                <v-btn text large color="red darken-2" @click="cancelUpload">Cancel</v-btn>
                                                <v-btn dark x-large color="primary" :loading="loading" @click="updateImg">Update Image</v-btn>
                                            </v-card-actions>
                                        </template>
                                        <template v-else>
                                            <v-progress-circular indeterminate color="primary lighten-2" :width="10" :size="70" justify="center" class="mx-auto mt-5"></v-progress-circular>
                                        </template>
                                    </template>
                                </v-card>

                                <v-card light flat elevation="6" min-height="400" class="mt-4 mb-6">
                                    <v-card-title class="primary white--text justify-center">
                                        Update Campaign Expiry
                                    </v-card-title>
                                    <v-card-text class="subtitle-1 mt-5 grey--text darken-4" align="start" >
                                        Please note that you can only update your campaign expiry date once in the lifecycle of that campaign.
                                    </v-card-text>
                                    <v-divider></v-divider>
                                    <v-card-text class="subtitle-1" align="start">
                                        Expiry Date: {{ campaign.expiry }}
                                    </v-card-text>
                                    <!-- <v-divider></v-divider> -->
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
                                </v-card>
                            </template>
                            <template v-else>
                                <v-alert border="left" type="error">
                                    You are not allowed to modify this campaign!
                                </v-alert>
                            </template>
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

export default {
    data() {
        return {
            id: this.$route.params.id,
            slug: this.$route.params.slug,
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
            expiryUpdated: false
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
                    this.campaign = res.data
                    this.showEdit = true
                }
            }).catch(() =>{
                this.isLoading = false
                this.invalidCampaign = true
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
                        setTimeout(() => {
                            this.$router.push({name: 'MyProfile'})
                        }, 3000);
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
                    // this.loading = false
                    this.campaign.picture = res.data.image
                    this.imageUploadSuccess = true
                    this.imageUpdating = true
                    setTimeout(() => {
                        this.$router.push({name: 'MyProfile'})
                    }, 3000);
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
        }
    },
    created() {
        this.getCampaign()
    },
}
</script>