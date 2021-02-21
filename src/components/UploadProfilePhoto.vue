<template>
    <div class="upload">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12" md="8">
                    <v-card light elevation="12" class="mt-6 pt-5 pb-5">
                        <v-card-title class="headline justify-center pt-5 primary--text darken--2">
                            Thank you for registering on Kolabo. Let's get to meet you!
                        </v-card-title>
                        <v-card-text class="title pt-5">To complete your registration, we request that you upload a picture of yourself to give your profile a human face.</v-card-text>
                        <v-card-text class="text-center">
                            <v-card-actions v-if="!previewImg" class="justify-center pt-6">
                                <v-btn large color="secondary" class="mb-5 ml-5" @click="openUpload">Choose A Picture</v-btn>
                                <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                            </v-card-actions>
                            <template class="py-5 px-3" v-if="previewImg">
                                <v-img :src="previewImgUrl" height="200" contain alt="Preview image" aspect-ratio="1"></v-img>
                                <div class="mt-5 mb-5">
                                    <v-btn text dark class="mb-5 mt-4 mr-2" color="red" @click.prevent="cancelUpload" width="30%">Cancel</v-btn>
                                    <v-btn large dark class="mb-5 mt-4" color="primary" @click.prevent="uploadImage" width="30%" :loading='isLoading'>Upload Picture</v-btn>
                                </div>
                            </template>
                        </v-card-text>
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
            previewImg: false,
            previewImgUrl: null,
            new_user: null,
            api: "http://localhost:8000/api/",
            isLoading: false
        }
    },
    computed: {
        authToken() {
            return this.$store.getters.getToken;
        },
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.authToken) {
                next("/");
            }
            if(localStorage.getItem('new_reg')){
                next()
            }else{
                next('/register')
            }
        });
    },
    methods: {
        openUpload(){
            this.$refs.image.click()
        },
        pickImg(e){
            const file = e.target.files[0]
            this.image = file
            this.previewImg = true
            this.previewImgUrl = URL.createObjectURL(file)
        },
        uploadImage(){
            if(this.image !== null){
                this.isLoading = true
                let form = new FormData();
                form.append('picture', this.image)
                form.append('new_user', this.new_user.email)

                this.$axios.put(this.api + 'profile_picture/upload/', form).then((res) => {
                    this.isLoading = false
                    console.log(res.data)
                    // this.profile.picture = res.data
                    localStorage.removeItem('new_reg')
                    this.$router.push({name: 'RegisteredSuccessfully'})
                    // this.imageUploadSuccess = true
                    this.cancelUpload()
                }).catch(() => {
                    this.loading = false
                })
            }
        },
        cancelUpload(){
            // this.$refs.image.value = ''
            this.previewImgUrl = '';
            this.previewImg = false;
        },
        getNewReg(){
            let reg = localStorage.getItem('new_reg')
            if(reg){
                this.new_user = JSON.parse(reg)
                console.log(JSON.parse(reg))
            }
        }
    },
    mounted() {
        this.getNewReg()
    },
}
</script>