<template>
    <div class="add_bank_details">
        <v-container>
            <v-row wrap justify="start">
                <v-col cols="3" md="3">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
                </v-col>
                <v-col cols="9" md="6">
                    <span class="title font-weight-bold" v-if="account">Account Details of {{ account.user && account.user.fullname }}</span>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="7">
                    <template v-if="!detailsForm">
                        <template v-if="account && account.status === 404">
                            <v-card tile min-height="100" class="mt-5">
                                <v-alert type="warning" border="left" class="mt-6">Hello {{ authUser.first_name }}, You have not added your bank account details to your profile</v-alert>
                                <v-card-actions class="justify-center">
                                    <v-btn text class="primary--text" large @click="detailsForm = true">Add Details</v-btn>
                                </v-card-actions>
                            </v-card>
                        </template>
                        <v-card v-else light flat outlined elevation="12" min-height="200" class="py-3">
                            <template v-if="!editDetails">
                                <v-card-text align="center" justify="center" class="ml-4">
                                    <table class="table table-hover table-striped table-condensed">
                                        <tbody>
                                            <tr align="left">
                                                <th width="30%">Bank</th>
                                                <td>{{ account.bank }}</td>
                                            </tr>
                                            <tr>
                                                <th>Account Type:</th>
                                                <td>{{ account.account_type }}</td>
                                            </tr>
                                            <tr>
                                                <th>Account Number:</th>
                                                <td>{{ account.account_number }}</td>
                                            </tr>
                                            <tr>
                                                <th>Account Name:</th>
                                                <td>{{ account.account_name }}</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </v-card-text>
                                <v-card-actions class="justify-center">
                                    <v-btn text class="primary--text" @click="editDetails = true"><v-icon>edit</v-icon></v-btn>
                                </v-card-actions>
                            </template>
                            <template v-else>
                                <v-card-title class="justify-center mb-3">Edit Bank Details</v-card-title>
                                <v-card-text align="start">
                                    <v-select label="Bank" :items="banks" v-model="account.bank" required v-validate="'required'" item-text="name" item-value="short_name" :error-messages="errors.collect('edit.bank')" name="bank" data-vv-scope="edit"></v-select>
                                    <v-select label="Account Type" :items="account_types" v-model="account.account_type" required v-validate="'required'" item-text="type" item-value="type" :error-messages="errors.collect('edit.account')" name="type" data-vv-scope="edit"></v-select>
                                    <v-text-field label="Account Number" v-model="account.account_number" required v-validate="'required|integer|min:10|max:10'" :error-messages="errors.collect('edit.number')" name="number" data-vv-scope="edit"></v-text-field>
                                    <v-text-field label="Account Name" v-model="account.account_name" required v-validate="'required|max:100'" :error-messages="errors.collect('edit.name')" name="number" data-vv-scope="edit"></v-text-field>
                                </v-card-text>
                                <v-card-actions class="justify-center mb-4">
                                    <v-btn large width="30%" text class="red--text" @click="editDetails = false">Cancel</v-btn>
                                    <v-btn large width="40%" class="primary white--text" :loading="isLoading" @click="updateDetails">Update Details</v-btn>
                                </v-card-actions>
                            </template>
                        </v-card>
                    </template>
                    <template v-if="detailsForm">
                        <v-card light elevation="12" min-height="350" class="py-3 px-3">
                            <v-card-title class="title justify-center">Add Bank Details</v-card-title>
                            <v-card-text>
                                <v-select label="Bank" v-model="account.bank" :items="banks" item-text="name" item-value="short_name" required persistent-hint v-validate="'required'" :error-messages="errors.collect('bank')" name="bank"></v-select>
                                <v-select label="Account Type" v-model="account.account_type" :items="account_types" item-text="type" item-value="type" required persistent-hint v-validate="'required'" :error-messages="errors.collect('type')" name="type"></v-select>
                                <v-text-field label="Account Number" v-model="account.account_number" required v-validate="'required|integer|min:10|max:10'" :error-messages="errors.collect('number')" name="number"></v-text-field>
                                <v-text-field label="Account Name" hint="Name as appearing on account" v-model="account.account_name" required v-validate="'required'" :error-messages="errors.collect('name')" name="name"></v-text-field>
                            </v-card-text>
                                <div class="subtitle-1 ml-4 mb-3 font-weight-bold" align="start">Upload Your ID Card</div>
                            <v-card-actions v-if="!previewImg">
                                <v-btn class="secondary--text mb-5 ml-5" @click="openUpload">Choose ID Card</v-btn>
                                <input type="file" ref="image" style="display:none" @change.prevent="pickImg" accept="image/*"> 
                            </v-card-actions>
                            <template class="py-5 px-3" v-if="previewImg">
                                <v-img :src="previewImgUrl" height="180" contain alt="Preview image"></v-img>
                                <div class="mt-2 mb-2">
                                    <v-btn text dark class="mb-5 mt-2 mr-2" color="red" @click.prevent="cancelUpload" width="30%">Cancel</v-btn>
                                    <!-- <v-btn large dark class="mb-5 mt-4" color="primary" @click.prevent="updateImage"  width="30%"><v-icon color="white" left>cloud</v-icon>Update</v-btn> -->
                                </div>
                            </template>
                            <v-card-actions class="justify-center mb-3">
                                <v-btn large light class="primary" width="40%" @click="submit" :loading="isLoading">Save</v-btn>
                            </v-card-actions>
                        </v-card>
                    </template>
                </v-col>
            </v-row>
            <v-snackbar v-model="bankDetailsAdded" :time="3500" top color="green darken-2 white--text">Your Bank Details have been added successfully. 
                <v-btn text color="white--text" @click="bankDetailsAdded = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="noIdcardUploaded" :time="6000" top color="red darken-2 white--text">You must upload a means of ID (Intn Passport, Nat.ID or Nat Drivers Licence). 
                <v-btn text color="white--text" @click="noIdcardUploaded = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="uploadFailed" :time="6000" top color="red darken-2 white--text">Bank details add failed. Please ensure you upload a valid means of ID. 
                <v-btn text color="white--text" @click="uploadFailed = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="detailUpdateFailed" :time="6000" top color="red darken-2 white--text">Bank details update failed. Please try again. 
                <v-btn text color="white--text" @click="detailUpdateFailed = false">Close</v-btn>
            </v-snackbar>
            <v-snackbar v-model="detailUpdated" :time="4000" top color="green darken-2 white--text">Bank details updated successfully. 
                <v-btn text color="white--text" @click="detailUpdated = false">Close</v-btn>
            </v-snackbar>
        </v-container>
    </div>
</template>

<script>
export default {
    data() {
        return {
            api: "http://localhost:8000/api/",
            account: {
                bank: '',
                account_type: '',
                account_number: null,
                account_name: '',
                id_card: null
            },
            detailsForm: false,
            banks: [],
            account_types: [
                {type: 'Savings'},
                {type: 'Current'},
                {type: 'Others'}
            ],
            previewImg: false,
            previewImgUrl: null,
            bankDetailsAdded: false,
            noIdcardUploaded: false,
            uploadFailed: false,
            isLoading: false,
            editDetails: false,
            detailUpdateFailed: false,
            detailUpdated: false
        }
    },
    computed: {
        authUser(){
            return this.$store.getters.getAuthUser
        },
        authToken() {
            return this.$store.getters.getToken;
        },
        isLoggedIn(){
            return this.$store.getters.isLoggedIn
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
        getLinkedAccount(){
            if(this.isLoggedIn){
                this.$axios.get(this.api + 'check-linked-account/', this.config).then((res) => {
                    console.log(res.data)
                    this.account = res.data
                })
            }
        },
        getBanks(){
            this.$axios.get(this.api + 'banks/', this.config).then((res) =>{
                this.banks = res.data
                console.log(res.data)
            })
        },
        openUpload(){
            this.$refs.image.click()
        },
        pickImg(e){
            const file = e.target.files[0]
            this.account.id_card = file
            this.previewImg = true
            this.previewImgUrl = URL.createObjectURL(file)
        },
        cancelUpload(){
            this.previewImgUrl = '';
            this.previewImg = false;
        },
        submit(){
            this.$validator.validateAll().then((isValid) =>{
                if(isValid){
                    if(this.account.id_card != null){
                        this.isLoading = true
                        let form = new FormData();
                        form.append('id_card', this.account.id_card)
                        form.append('bank', this.account.bank)
                        form.append('account_type', this.account.account_type)
                        form.append('account_number', this.account.account_number)
                        form.append('account_name', this.account.account_name)

                        this.$axios.post(this.api + 'add-bank-details/', form, this.fullHeader)
                        .then((res) => {
                            this.isLoading = false
                            console.log(res.data)
                            this.bankDetailsAdded = true
                            setTimeout(() => {
                                this.$router.push({name: 'MyProfile'})
                            }, 2500);
                        }).catch(() => {
                            this.isLoading = false
                            this.uploadFailed = true
                        })
                    }else{
                        this.isLoading = false
                        this.noIdcardUploaded = true
                    }
                }
            })
        },
        updateDetails(){
            this.$validator.validateAll('edit').then((isValid) =>{
                if(isValid){
                    console.log(this.account)
                    this.isLoading = true
                    this.$axios.patch(this.api + 'update-bank-details/', {
                        bank: this.account.bank,
                        account_type: this.account.account_type,
                        account_number: this.account.account_number,
                        account_name: this.account.account_name,
                    }, this.config)
                    .then((res) => {
                        this.isLoading = false
                        this.account = res.data
                        console.log(res.data)
                        this.editDetails = false
                        this.detailUpdated = true
                    }).catch(() => {
                        this.isLoading = false
                        this.detailUpdateFailed = true
                    })
                }
            })
        }
    },
    mounted() {
        this.getLinkedAccount()
        this.getBanks()
    },
}
</script>