<template>
    <div class="success_story mt-n5">
        <template v-if="campaign.paid">
            <template v-if="!isLoading">
                <v-row wrap justify="start">
                    <v-col cols="12" md="8">
                        <template v-if="story">
                            <template v-if="!edit">
                                <v-card-title class="align-start title ml-3">{{ story.title | capFirstLetter }}</v-card-title>
                                <v-card-text align="start" class="subtitle-1 ml-3 mt-2">{{ story.details | capFirstLetter }}</v-card-text>
                                <v-card-actions class="justify-center">
                                    <v-btn text color="red darken-2" @click="delDial = true"><v-icon>delete_forever</v-icon></v-btn>
                                    <v-btn dark text color="primary" @click="edit = true"><v-icon>edit</v-icon></v-btn>
                                </v-card-actions>
                            </template>
                            <template v-else>
                                <v-card-text>
                                    <v-text-field label="Title" v-model="story.title" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                                    <v-textarea label="Details" rows="2" auto-grow v-model="story.details" required v-validate="'required|min:10|max:400'" :error-messages="errors.collect('details')" name="details"></v-textarea>
                                </v-card-text>
                                <v-card-actions class="justify-center mt-2">
                                    <v-btn text large color="red darken-2" width="25%" @click="edit = false">Cancel</v-btn>
                                    <v-btn dark large color="primary" width="30%" :loading="updating" @click="update">Update</v-btn>
                                </v-card-actions>
                            </template>
                        </template>
                        <template v-else>
                            <template v-if="!addNew">
                                <v-alert type="info">
                                    You have not written a success story for your campaign.
                                </v-alert>
                                <v-card-actions class="justify-center mt-2">
                                    <v-btn dark large color="primary" @click="addNew = true">Add Success Story</v-btn>
                                </v-card-actions>
                            </template>
                            <template v-else>
                                <v-card-text class="mt-2">
                                    <v-text-field label="Title" v-model="newStory.title" required v-validate="'required|min:10|max:150'" :error-messages="errors.collect('title')" name="title"></v-text-field>
                                    <v-textarea label="Details" v-model="newStory.details" rows="2" auto-grow required v-validate="'required|min:10|max:400'" :error-messages="errors.collect('details')" name="details"></v-textarea>
                                </v-card-text>
                                <v-card-actions class="justify-center mt-2 pb-5">
                                    <v-btn text color="red darken-2" width="25%">Cancel</v-btn>
                                    <v-btn dark large color="primary" width="35%" :loading="isLoading" @click="saveNewStory">Save</v-btn>
                                </v-card-actions>
                            </template>
                        </template>
                    </v-col>
                </v-row>
            </template>
            <v-progress-circular v-else indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
        </template>
        <template v-else>
            <v-row wrap align="start">
                <v-col cols="12" md="8">
                    <v-alert type="info" class="ml-5">
                        You are not allowed to write success story until after your campaign is completed and you have been paid.
                    </v-alert>
                </v-col>
            </v-row>
        </template>
        <v-dialog v-model="delDial" max-width="430">
            <v-card>
                <v-card-title class="title justify-center">Do you really want to delete this success story?</v-card-title>
                <v-card-text class="subtitle-1" align="start">
                    You will not be able to recover it if you proceed to delete.
                </v-card-text>
                <v-card-actions class="justify-center pb-5">
                    <v-btn text dark color="red darken-1" @click="delDial = false"> Cancel</v-btn>
                    <v-btn dark color="primary" @click="delStory" :loading="isDeleting">Yes, Delete</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="editSuccess" :time="5000" top color="green darken-2 white--text">Your campaign success story has been updated successfully.
            <v-btn text color="white--text" @click="editSuccess = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="editFail" :time="5000" top color="red darken-2 white--text">Your campaign success story was not updated. Please try again.
            <v-btn text color="white--text" @click="editFail = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="delSuccess" :time="5000" top color="green darken-2 white--text">Your campaign success story has been deleted.
            <v-btn text color="white--text" @click="delSuccess = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="delFail" :time="5000" top color="red darken-2 white--text">Your campaign success story cannot be deleted. Please try again.
            <v-btn text color="white--text" @click="delFail = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="storyCreated" :time="5000" top color="green darken-2 white--text">Your campaign success story has been created successfully.
            <v-btn text color="white--text" @click="storyCreated = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="storyCreateFail" :time="5000" top color="red darken-2 white--text">Your campaign success story failed to create. Please try again.
            <v-btn text color="white--text" @click="storyCreateFail = false">Close</v-btn>
        </v-snackbar>
    </div>
</template>

<script>
export default {
    props: ['campaign'],
    data() {
        return {
            story: null,
            api: "http://localhost:8000/api/",
            isLoading: false,
            delDial: false,
            isDeleting: false,
            edit: false,
            editStory: {
                title: '',
                details: ''
            },
            updating: false,
            editSuccess: false,
            editFail: false,
            delSuccess: false,
            delFail: false,
            addNew: false,
            newStory: {
                title: '',
                details: ''
            },
            storyCreated: false,
            storyCreateFail: false
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
    },
    methods: {
        getStory(){
            this.isLoading = true
            this.$axios.get(this.api + `success_story/${this.campaign.id}/`, this.config)
            .then((res) => {
                this.isLoading = false
                if(res.data.status === 404){
                    this.story = null
                }else{
                    this.story = res.data
                }
            })
        },
        delStory(){
            this.isDeleting = true
            this.$axios.delete(this.api + `delete_story/${this.story.id}/`, this.config)
            .then((res) => {
                this.isDeleting = false
                this.delDial = false
                this.delSuccess = true
                this.story = null
                console.log(res.data)
            }).catch(() =>{
                this.isDeleting = false
                this.delFail = true
            })
        },
        update(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.updating = true
                    this.$axios.patch(this.api + `update_story/${this.story.id}/`, {
                        title: this.story.title,
                        details: this.story.details,
                    }, this.config)
                    .then((res) => {
                        this.updating = false
                        this.story = res.data
                        this.edit = false
                        this.editSuccess = true
                        console.log(res.data)
                    }).catch(() => {
                        this.updating = false
                        this.editFail = true
                    })
                }
            })
        },
        saveNewStory(){
            this.$validator.validateAll().then((isValid) => {
                if (isValid) {
                    this.isLoading = true
                    this.$axios.post(this.api + `add_story/${this.campaign.id}/`, {
                        title: this.newStory.title,
                        details: this.newStory.details
                    }, this.config)
                    .then((res) => {
                        this.isLoading = false
                        console.log(res.data)
                        this.storyCreated = true
                        this.story = res.data 
                    })
                }
            })
        }
    },
    created() {
        this.getStory()
    },
}
</script>