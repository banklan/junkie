<template>
    <div class="profile">
        <v-container>
            <v-row wrap justify="start">
                <v-col cols="6" md="3">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
                </v-col>
                <v-col cols="6" md="6">
                    <span class="headline">Profile Page</span>
                </v-col>
            </v-row>
            
            <v-row wrap justify="space-around">
                <v-col cols="12" md="7">
                    <v-card elevation="12" light min-height="500" v-if="profile" class="pb-5">
                        <v-card-title dark class="primary white--text title justify-center mb-4">{{ profile.fullname }}</v-card-title>
                        <template v-if="!edit">
                            <v-img contain aspect-ratio="1" :src="profile.picture" height="300"></v-img>
                            <v-card-text align="center" justify="center" class="ml-4">
                                <v-simple-table fixed-header min-height="150px" v-if="profile">
                                    <template v-slot:default>
                                        <tr align="left" height="30">
                                            <th width="30%">First Name</th>
                                            <td>{{ profile.first_name }}</td>
                                        </tr>
                                        <tr align="left" height="30">
                                            <th>Last Name</th>
                                            <td>{{ profile.last_name }}</td>
                                        </tr>
                                        <tr align="left" height="30">
                                            <th>Email</th>
                                            <td>{{ profile.email }}</td>
                                        </tr>
                                        <tr align="left" height="30">
                                            <th>Phone Number:</th>
                                            <td>{{ profile.phone_no }}</td>
                                        </tr>
                                        <tr align="left" height="30">
                                            <th>Location</th>
                                            <td>{{ profile.location }}</td>
                                        </tr>
                                        <tr align="left" height="40">
                                            <th><router-link to="/profile/bank_details">Bank Details</router-link></th>
                                        </tr>
                                    </template>
                                </v-simple-table>
                            </v-card-text>
                            <v-card-actions class="justify-center pb-5">
                                <v-btn @click="editPr" class="blue lighten--2 white--text mr-3"><v-icon class="white--text">edit</v-icon></v-btn>
                                <v-btn class="purple darken-2 white--text"  @click="openPswdDialg = true">Change Password</v-btn>
                                <v-btn class="pink darken-2 white--text" @click="disableConfirm = true">Disable Profile</v-btn>
                            </v-card-actions>
                        </template>
                        <template v-else>
                            <v-card-title align="center" class="ml-4 title">Update Profile</v-card-title>
                            <v-card-text>
                                <v-text-field label="First Name" v-model="updtProfile.first" v-validate="'required'" :error-messages="errors.collect('editNames.first')" name="first" data-vv-scope="editProf"></v-text-field>
                                <v-text-field label="Last Name" v-model="updtProfile.last" v-validate="'required'" :error-messages="errors.collect('editNames.last')" name="last" data-vv-scope="editProf"></v-text-field>
                                <v-text-field label="Phone No" v-model="updtProfile.phone" v-validate="'required'" :error-messages="errors.collect('editNames.phone')" name="last" data-vv-scope="editProf"></v-text-field>
                            </v-card-text>
                            <v-card-actions class="justify-center mb-5 flex-wrap pa-5 ml-3">
                                <v-btn text dark color="red" @click="edit = false" width="30%">Cancel</v-btn>
                                <v-btn large class="primary white--text ml-2" width="30%" @click="updateProfile" :loading="isUpdating">Update</v-btn>
                            </v-card-actions>
                            <v-divider></v-divider>
                            <v-card-title class="justify-start ml-4 title">Replace profile Picture</v-card-title>
                            <v-card-actions v-if="!previewImg">
                                <v-btn large color="secondary" class="mb-5 ml-5" @click="openUpload">Choose New Picture</v-btn>
                                <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                            </v-card-actions>
                            <template class="py-5 px-3" v-if="previewImg">
                                <v-img :src="previewImgUrl" height="200" contain alt="Preview image" aspect-ratio="1"></v-img>
                                <div class="mt-5 mb-5">
                                    <v-btn text dark class="mb-5 mt-4 mr-2" color="red" @click.prevent="cancelUpload" width="30%">Cancel</v-btn>
                                    <v-btn large dark class="mb-5 mt-4" color="primary" @click.prevent="updateImage"  width="30%"><v-icon color="white" left>cloud</v-icon>Update</v-btn>
                                </div>
                            </template>
                        </template>
                    </v-card>
                    <profile-campaigns :profile="profile"></profile-campaigns>

                </v-col>
                <v-col cols="12" md="5">
                    <my-donations></my-donations>
                </v-col>
            </v-row>
            <v-dialog v-model="openPswdDialg" max-width="420">
                <v-card>
                    <v-card-title class="title justify-center">Change Password</v-card-title>
                    <v-card-subtitle v-if="pswdChngErr" class="text-center py-2 mx-2 pink lighten-4 red--text">{{ pswdErr }}</v-card-subtitle>
                    <v-card-text>
                        <v-text-field label="Old Password" type="password" v-model="passwordChange.old" v-validate="'required|max:20|min:5'" :error-messages="errors.collect('pswdChang.old_pswd')" name="old_pswd" data-vv-as="Old Password" data-vv-scope="pswdChang"></v-text-field>
                        <v-text-field label="New Password" type="password" v-model="passwordChange.new" v-validate="'required|max:20|min:5'" :error-messages="errors.collect('pswdChang.new_pswd')" name="new_pswd" ref="new_pswd" data-vv-as="new password" data-vv-scope="pswdChang"></v-text-field>
                        <v-text-field label="Confirm New Password" type="password" v-model="passwordChange.confirm" v-validate="'required|confirmed:new_pswd'" :error-messages="errors.collect('pswdChang.confirm')" name="confirm" data-vv-as="confirm password" data-vv-scope="pswdChang"></v-text-field>
                    </v-card-text>
                    <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn text dark color="red darken-1" @click.prevent="removePswdDialog"> Cancel </v-btn>
                        <v-btn dark :loading="loading" color="primary" @click="changePswd" width="50%">Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-dialog v-model="disableConfirm" max-width="500">
                <v-card>
                    <v-card-title class="title justify-center">Are you sure you want to disable your account?</v-card-title>
                    <v-card-text class="body-2">
                        <v-alert type="warning">To enable it and have access to your account back, you have to contact us.</v-alert>
                    </v-card-text>
                    <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn text dark color="red darken-1" @click="disableConfirm = false"> Cancel </v-btn>
                        <v-btn dark :loading="loading" color="primary" @click="disableAccount">Yes, Disable</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-snackbar v-model="profileUpdateSuccess" :time="5000" top color="green darken-2 white--text">Profile has been updated successfully. 
                <v-btn text color="white--text" @click="profileUpdateSuccess = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="profileUpdateFail" :time="5000" top color="red darken-2 white--text">Profile update failed. Please try again. 
                <v-btn text color="white--text" @click="profileUpdateFail = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="imageUploadSuccess" :time="5000" top color="green darken-2 white--text">Profile picture updated ssuccessfully. 
                <v-btn text color="white--text" @click="imageUploadSuccess = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="imageUploadFail" :time="5000" top color="red darken-2 white--text">Profile picture update failed. Please try again. 
                <v-btn text color="white--text" @click="imageUploadFail = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="pswdUpdateSuccess" :time="5000" top color="green darken-2 white--text">Your password has been updated successfully. 
                <v-btn text color="white--text" @click="pswdUpdateSuccess = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="disabledSuccess" :time="3000" top color="green darken-2 white--text">Your Account has been disabled. 
                <v-btn text color="white--text" @click="disabledSuccess = false">Close</v-btn>
            </v-snackbar>
        </v-container>
    </div>
</template>


<script>
export default {
    data(){
        return {
            profile: null,
            api: "http://localhost:8000/api/",
            edit: false,
            updtProfile:{
                first: '',
                last: '',
                phone: ''
            },
            profileUpdateSuccess: false,
            profileUpdateFail: false,
            isUpdating: false,
            loading: false,
            image: null,
            previewImg: false,
            previewImgUrl: '',
            imageUploadSuccess: false,
            imageUploadFail: false,
            openPswdDialg: false,
            pswdChngErr: false,
            passwordChange: {
                old: '',
                new: '',
                confirm: ''
            },
            pswdErr: null,
            pswdUpdateSuccess: false,
            disableConfirm: false,
            disabledSuccess: false
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
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.authToken) {
                next();
            }else{
                next('/')
            }
        });
    },
    methods: {
        getProfile(){
            this.$axios.get(this.api + 'profile/', this.config).then((res) => {
                this.profile = res.data
                // console.log(res.data)
            })
        },
        editPr(){
            this.edit = true
            this.updtProfile.first = this.profile.first_name
            this.updtProfile.last = this.profile.last_name
            this.updtProfile.phone = this.profile.phone_no
        },
        updateProfile(){
            this.$validator.validateAll("editProf").then((isValid) => {
                if (isValid) {
                    this.isUpdating = true
                    this.$axios.patch(this.api + 'profile/update/', {
                        first_name: this.updtProfile.first,
                        last_name: this.updtProfile.last,
                        phone_no: this.updtProfile.phone,
                    }, this.config).then((res) => {
                        this.isUpdating = false
                        // console.log(res.data)
                        this.edit = false
                        this.profile = res.data
                        this.profileUpdateSuccess = true
                    }).catch(() => {
                        this.isUpdating = false
                        this.profileUpdateFail = true
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
        updateImage(){
            if(this.image !== null){
                this.loading = true
                let form = new FormData();
                form.append('picture', this.image)

                this.$axios.put(this.api + 'profile_image/update/', form, this.fullHeader).then((res) => {
                    this.loading = false
                    // console.log(res.data)
                    this.profile.picture = res.data
                    this.imageUploadSuccess = true
                    this.cancelUpload()
                    this.edit = false
                    this.getProfile()
                }).catch(() => {
                    this.loading = false
                    this.imageUploadFail = true
                })
            }
        },
        cancelUpload(){
            // this.$refs.image.value = ''
            this.previewImgUrl = '';
            this.previewImg = false;
        },
        changePswd(){
            this.$validator.validateAll('pass').then((isValid) =>{
                if(isValid){
                    this.loading = true
                    if(this.passwordChange.old != this.passwordChange.new){
                        this.$axios.put(this.api + 'password-change/', {
                            password: this.passwordChange.old,
                            new_password: this.passwordChange.new,
                            confirm_password: this.passwordChange.confirm
                        }, this.config).then(() => {
                            this.loading =  false
                            this.pswdUpdateSuccess = true
                            this.removePswdDialog()
                        }).catch(() => {
                            this.loading = false
                            this.pswdChngErr = true
                            this.pswdErr = 'Password change failed. Your old password might be wrong!'
                        })
                    }else{
                        this.loading = false
                        this.pswdChngErr = true
                        this.pswdErr = 'The new password is the same with the old password you are trying to change!'
                    }
                }
            })
        },
        removePswdDialog(){
            this.openPswdDialg = false
            this.$validator.reset()
            this.passwordChange.old = ''
            this.passwordChange.new = ''
            this.passwordChange.confirm = ''
            this.pswdChngErr = false
            this.pswdErr = ''
        },
        disableAccount(){
            this.loading = true
            this.$axios.put(this.api + 'disable-account/', {}, this.config).then(() => {
                this.loading = false
                setTimeout(() => {
                    this.disabledSuccess = true
                }, 3000);
                this.logout()
            }).catch(() => {
                this.loading = false
            })
        },
        logout() {
            if (this.authToken) {
                this.$store.commit("logout");
                if (this.$route.path != "/") {
                    this.$router.push("/");
                }
            }
        }
    },
    created(){
        this.getProfile()
    }
}
</script>

<style scoped lang="scss">
    .profile th a{
        text-decoration: none !important;
        transition: all .4s;

        &:hover{
            color: rgb(221, 79, 13);
        }
    }
    
</style>