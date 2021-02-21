<template>
    <div class="add_update">
        <template v-if="updateForm">
            <v-card-title align="start">Add New Update</v-card-title>
            <v-card-text align="start" class="mt-3 mb-3">
                <v-text-field label="Title" v-model="newUpdate.title" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                <v-textarea label="Details" rows="2" auto-grow v-model="newUpdate.details" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('details')" name="details"></v-textarea>
            </v-card-text>
            <v-card-actions class="justify-center mt-3 pb-4">
                <v-btn large text dark color="red darken-2" width="30%">Cancel</v-btn>
                <v-btn large dark color="primary" width="30%" :loading="isLoading" @click="saveNewUpdate">Save</v-btn>
            </v-card-actions>
        </template>
        <template v-else>
            <v-alert type="success" v-if="!imageUploaded">
                Your new update has been submitted. Kindly upload an image for the update.
            </v-alert>
            <v-card-text justify="start" class="mt-2 mb-3">
                <template v-if="!previewImg">
                    <v-btn outlined color="primary" @click="openUpload" class="mr-3">Browse Picture</v-btn>
                    <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*">
                    <v-btn outlined color="secondary" @click="clearForm">No Picture</v-btn>
                </template>
                <template v-else>
                    <template v-if="!imageUploaded">
                        <div class="justify-center mt-3 mb-3 subtitle-1">Preview Image</div>
                        <div class="preview">
                            <div class="img ml-5">
                                <v-img :src="previewImgUrl" height="120" alt="Preview image" aspect-ratio="1"></v-img>
                            </div>
                            <v-btn color="red darken-2" text @click="removeImg"><v-icon>delete_forever</v-icon></v-btn>
                        </div>
                        <v-card-actions class="mt-3 pb-3" align="start" justify="start">
                            <v-btn text color="red darken-2" @click="removeImg">Cancel Upload</v-btn>
                            <v-btn dark color="primary" @click="uploadImg" :loading="isLoading">Save Picture</v-btn>
                        </v-card-actions>
                    </template>
                    <template v-else>
                        <v-alert type="success" border="left">
                            Your picture has been uploaded successfully.
                        </v-alert>
                    </template>
                </template>
            </v-card-text>
        </template>
        <v-snackbar v-model="updatedSaved" :time="5000" top color="green darken-2 white--text">The update has been deleted.  
            <v-btn text color="white--text" @click="updatedSaved = false">Close</v-btn>
        </v-snackbar>
        
    </div>
</template>

<script>
import EventBus from '../../bus'

export default {
    props: ['campaign'],
    data() {
        return {
            newUpdate: {
                title: '',
                details: '',
                image: null
            },
            api: "http://localhost:8000/api/",
            previewImg: false,
            previewImgUrl: null,
            isLoading: false,
            updatedSaved: false,
            updateForm: true,
            update: null,
            imageUploaded: false
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
    },
    methods: {
        openUpload(){
            this.$refs.image.click()
        },
        pickImg(e){
            const file = e.target.files[0]
            this.newUpdate.image = file
            this.previewImg = true
            this.previewImgUrl = URL.createObjectURL(file)
        },
        removeImg(){
            this.previewImg = false
            this.previewImgUrl = ''
            this.newUpdate.image = null
        },
        saveNewUpdate(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.isLoading = true
                    this.$axios.post(this.api + `add-update/${this.campaign.id}/`, {
                        title: this.newUpdate.title.trim(),
                        details: this.newUpdate.details.trim(),
                    }, this.config).then((res) => {
                        this.isLoading = false
                        this.updateForm = false
                        this.update = res.data
                        console.log(res.data)
                    }).catch(() => {
                        this.isLoading = false
                    })
                }
            })
        },
        uploadImg(){
            if(this.newUpdate.image !== null){
                // console.log(this.newUpdate.image)
                this.isLoading = true
                let form = new FormData();
                form.append('image', this.newUpdate.image)
                this.$axios.patch(this.api + `add-update-image/${this.update.id}/`, form, this.fullHeader)
                .then((res) => {
                    this.isLoading = false
                    console.log(res.data)
                    this.update = res.data
                    this.imageUploaded = true
                    setTimeout(() => {
                        this.clearForm()
                    }, 2000);
                })
            }
        },
        clearForm(){
            EventBus.$emit('clear-form', this.update)
        }
    },
}
</script>

<style lang="scss" scoped>
    .preview{
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 180px;
        height: 100px;
        .img{
            flex: 0 1 80%;
            height: 100%;
            border: 1px solid rgb(173, 173, 173) !important;
            border-radius: 6px;
            overflow: hidden;
            margin-right: 10px !important;
            .v-img{
                height: 100%;
                width: 100%;
            }
        }
        .v-btn{
            // flex: 0 1 30%;
        }
    }  
</style>