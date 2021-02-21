<template>
    <div class="campaign_update">
        <v-card outlined light flat min-height="200" class="mb-3">
            <template v-if="!edit">
                <v-row align="center">
                    <v-col cols="12" md="5">
                        <v-img :src="img" transition="scale-transition" aspect-ratio="1" alt="Update Image"></v-img>
                    </v-col>
                    <v-col cols="12" md="7">
                        <v-card-title class="justify-center title">{{ update.title | capFirstLetter }}</v-card-title>
                        <v-card-text class="font-italic justify-center subtitle-2 mt-n3">{{ update.date }}</v-card-text>
                        <v-card-text class="mt-2 subtitle-1" align="start">{{ update.details | capFirstLetter }}</v-card-text>
                        <v-card-actions class="justify-center">
                            <v-btn text light color="red darken-2" @click="confirmDelUpdate(update, index)"><v-icon>delete_forever</v-icon></v-btn>
                            <v-btn text light color="primary" @click="edit = true"><v-icon>edit</v-icon></v-btn>
                        </v-card-actions>
                    </v-col>
                </v-row>
            </template>
            <template v-else>
                <v-card-text class="mt-4" align="start">
                    <v-text-field label="Title" v-model="update.title" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                    <v-textarea label="Details" auto-grow rows="3" v-model="update.details" required v-validate="'required|min:10|max:400'" :error-messages="errors.collect('details')" name="details"></v-textarea>
                    <template v-if="!previewImg">
                        <v-btn outlined color="primary" class="mt-3" @click="openUpload">Change Picture</v-btn>
                        <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*">
                    </template>
                    <template v-else>
                        <div class="justify-center mt-3 mb-3 subtitle-1">Preview New Image</div>
                        <div class="preview">
                            <div class="img ml-5">
                                <v-img :src="previewImgUrl" height="120" alt="Preview image" aspect-ratio="1"></v-img>
                            </div>
                            <v-btn color="red darken-2" text @click="removeImg"><v-icon>delete_forever</v-icon></v-btn>
                        </div>
                    </template>
                </v-card-text>
                <v-card-actions class="justify-center pb-5 mt-3">
                    <v-btn text color="red darken-2" @click="edit = false">Cancel</v-btn>
                    <v-btn dark color="primary" width="33%" :loading="isLoading" @click="saveUpdate">Save</v-btn>
                </v-card-actions>                                             
            </template>
        </v-card>
        <v-dialog v-model="updateDelDial" max-width="450">
            <v-card>
                <v-card-title class="title justify-center">Do you really want to delete this update?</v-card-title>
                <v-card-text class="subtitle-1" align="start">
                    You will not be able to recover the update if you proceed to delete it.
                </v-card-text>
                <v-card-actions class="justify-center mb-5">
                    <v-btn text dark color="red darken-1" @click="updateDelDial = false"> Cancel</v-btn>
                    <v-btn dark color="primary" @click="delUpdate" :loading="isDeleting">Yes, Delete</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="updtDeleted" :time="5000" top color="green darken-2 white--text">The update has been deleted.  
            <v-btn text color="white--text" @click="updtDeleted = false">Close</v-btn>
        </v-snackbar>
    </div>
</template>

<script>
import EventBus from '../../bus'

export default {
    props: ['update', 'index'],
    data() {
        return {
            updateDelDial: false,
            updateSelected: null,
            indexToDel: null,
            updtDeleted: false,
            isDeleting: false,
            api: "http://localhost:8000/api/",
            edit: false,
            new_img: null,
            previewImg: false,
            previewImgUrl: null,
            isLoading: false,
            img: this.update.image
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
        confirmDelUpdate(updt, i){
            this.updateDelDial = true
            this.updateSelected = updt
            this.indexToDel = i
        },
        delUpdate(){
            let updt = this.updateSelected.id
            let index = this.indexToDel
            this.isDeleting = true
            this.$axios.delete(this.api + `update_delete/${updt}/`, this.config)
            .then((res) => {
                console.log(res.data)
                this.isDeleting = false
                this.updateDelDial = false
                this.updtDeleted = true
                EventBus.$emit('remove-del', index)
            }).catch(() => {
                this.isDeleting = false
            })
        },
        editUpdate(update){
            console.log(update)
        },
        openUpload(){
            this.$refs.image.click()
        },
        pickImg(e){
            const file = e.target.files[0]
            this.new_img = file
            this.previewImg = true
            this.previewImgUrl = URL.createObjectURL(file)
        },
        removeImg(){
            this.previewImg = false
            this.previewImgUrl = ''
        },
        saveUpdate(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.isLoading = true
                    if(this.new_img === null){
                        this.$axios.put(this.api + `modify_update/${this.update.id}/`, {
                            title: this.update.title,
                            details: this.update.details
                        }, this.config).then((res) =>{
                            this.isLoading = false
                            console.log(res.data)
                            this.edit = false
                        }).catch(() =>{
                            this.isLoading = false
                        })
                    }else{
                        // console.log(this.new_img)
                        let form = new FormData();
                        form.append('title', this.update.title)
                        form.append('details', this.update.details)
                        form.append('image', this.new_img)

                        this.$axios.patch(this.api + `modify_update/${this.update.id}/`, form, this.fullHeader)
                        .then((res) => {
                            this.isLoading = false
                            this.edit = false
                            console.log(res.data)
                            this.removeImg()
                            this.img = res.data.image
                        }).catch(() => {
                            this.isLoading = false
                        })
                    }
                }
            })
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
    }
</style>