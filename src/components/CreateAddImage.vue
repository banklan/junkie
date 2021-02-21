<template>
    <div class="checked_out">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12">
                    <div class="headline mb-5">Add Campaign Picture</div>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="9">
                    <v-card light outlined min-height="200" class="px-6 py-4">
                        <v-card-title class="title justify-center mb-6 primary--text">
                            Didn't they say a picture is worth more than a thousand words? Upload a picture for your campaign.
                        </v-card-title>
                        <template v-if="!previewImg">
                            <v-card-text class="mt-5">
                                <v-btn large outlined color="secondary" class="mb-5 mr-5" @click="openUpload">Upload Image</v-btn>
                                <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                            </v-card-text>
                        </template>
                        <template v-else>
                            <v-card-subtitle class="text-center subtitle-1 mt-5 mb-3">Preview Image</v-card-subtitle>
                            <img :src="previewImgUrl" height="200" alt="campaign image preview">
                            <v-card-title class="mt-3">
                                <v-alert type="info" border="left">By clicking on "Upload Image", you are consenting and agreeing to our <router-link to="/terms-conditions">Terms </router-link> and <router-link to="/privacy-policy">Privacy Policy</router-link>.</v-alert>
                            </v-card-title>  
                            <v-card-actions class="justify-center ml-n3">
                              <v-btn text small @click="removeImg"><v-icon color="red darken-2">delete</v-icon></v-btn> 
                              <v-btn large @click="submit" class="primary" :loading="isLoading"> Upload Image & Submit</v-btn> 
                            </v-card-actions>
                        </template>
                        <template v-if="imageUploaded">
                            <v-alert type="success" border="left">Image was uploaded successfully. </v-alert>
                        </template>
                    </v-card>
                </v-col>
            </v-row>
            <v-snackbar v-model="campaignSaved" :time="5000" top color="green darken-2 white--text">Congratulations, your campaign was created successfully.  
                <v-btn text color="white--text" @click="campaignSaved = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="createError" :time="12000" top color="red darken-2 white--text">There is an error while trying to create your campaign. Please check your details and ensure your network is ok before trying again.  
                <v-btn text color="white--text" @click="createError = false">Close</v-btn>
            </v-snackbar>
        </v-container>
    </div>
</template>


<script>
export default {
    data() {
        return {
            image: null,
            api: "http://localhost:8000/api/",
            isLoading: false,
            previewImg:  false,
            previewImgUrl: null,
            newCampaign: {},
            campaignSaved: false,
            imageUploaded: false,
            createError: false
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
        authToken() {
            return this.$store.getters.getToken;
        },
        config(){
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
    },
    methods: {
        submit(){
            if(this.newCampaign !== null){
                this.isLoading = true
                this.$axios.post(this.api + 'create-project/', {
                    title: this.newCampaign.title,
                    details: this.newCampaign.details,
                    beneficiary: this.newCampaign.beneficiary,
                    goal: this.newCampaign.goal,
                    expiry: this.newCampaign.expiry,
                    category: this.newCampaign.category,
                }, this.config)
                .then((res) => {
                    this.isLoading = false
                    localStorage.removeItem('new_campaign')
                    console.log(res.data)
                    this.uploadImage(res.data.result)
                }).catch((err) => {
                    this.isLoading = false
                    console.log(err)
                    this.createError = true
                })
            }
        },
        uploadImage(camp){
            if(this.image !== null){
                let form = new FormData();
                form.append('image', this.image)
                this.$axios.put(this.api + `create-project-image/${camp.id}/`, form, this.fullHeader).then((res) => {
                    console.log(res.data)
                    this.imageUploaded = true
                    this.campaignSaved = true
                    setTimeout(() => {
                        this.$router.push({name: 'CampaignShow', params: {id: camp.id, slug: camp.slug}})
                    }, 3500);
                })
            }
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
        removeImg(){
            // this.$refs.image.value = ''
            this.image = null
            this.previewImgUrl = '';
            this.previewImg = false;
        },
        getStoredData(){
            const data = localStorage.getItem('new_campaign')
            const stored = data ? JSON.parse(data) : null
            if(data){
                this.newCampaign = stored
            }else{
                this.$router.push({name: 'CreateNew'})
            }
        },
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