<template>
    <div class="login">
        <v-container>
            <v-row wrap justify="center">
                <v-col cols="12" md="7">
                    <v-card light shaped elevation="6" min-height="350">
                        <v-card-title class="title primary white--text justify-center">Register</v-card-title>
                        <div class="subtitle-2 red--text mt-5">**Please note that all fields are compulsory</div>
                        <v-card-text class="mt-3 mx-3">
                            <v-text-field label="First Name" v-model="user.f_name" required v-validate="'required|min:2|max:50'" :error-messages="errors.collect('f_name')" name="f_name" data-vv-as="first name"></v-text-field>
                            <v-text-field label="Last Name" hint="Family Name" v-model="user.l_name" required v-validate="'required|min:2|max:50'" :error-messages="errors.collect('l_name')" name="l_name" data-vv-as="last name"></v-text-field>
                            <v-text-field label="Email Address" v-model="user.email" required v-validate="'required|email'" :error-messages="errors.collect('email')" name="email"></v-text-field>
                            <v-row>
                                <v-col cols="12" md="6">
                                    <v-text-field label="Phone Number" v-model="user.phone" required v-validate="'required|integer'" :error-messages="errors.collect('phone')" name="phone" data-vv-as="phone number"></v-text-field>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <v-select label="Gender" v-model="user.gender" :items="gender" item-text="name" item-value="value" required v-validate="'required'" :error-messages="errors.collect('gender')" name="gender"></v-select>
                                </v-col>
                            </v-row>
                            <v-text-field label="Street Address" hint="Example: No 2" v-model="user.location1" required v-validate="'required|min:1|max:20'" :error-messages="errors.collect('location1')" name="location1" data-vv-as="Street number"></v-text-field>
                            <v-text-field label="Address" hint="ABC Street, off XYZ Road" v-model="user.location2" required v-validate="'required|min:5|max:80'" :error-messages="errors.collect('location2')" name="location2" data-vv-as="street address"></v-text-field>
                            <v-text-field label="Town/City/State" hint="Town/City, State" v-model="user.state" required v-validate="'required|min:3|max:80'" :error-messages="errors.collect('location3')" name="location3" data-vv-as="town/city/state"></v-text-field>
                            <v-text-field type="password" label="Password" v-model="user.password" required ref="password" v-validate="'required|min:5|max:30'" :error-messages="errors.collect('password')" name="password"></v-text-field>
                            <v-text-field type="password" label="Confirm Password" v-model="user.c_password" required v-validate="'required|confirmed:password'" :error-messages="errors.collect('c_password')" name="c_password" data-vv-as="confirm password"></v-text-field>
                        </v-card-text>
                        <v-card-text class="mt-n7 ml-2">
                            <v-checkbox v-model="checkbox" required label="I agree to the Terms & Policy"></v-checkbox>
                            <v-alert type="error" v-if="agreeToTerms" align="left">{{ agreeValdtn }}</v-alert>
                        </v-card-text>
                        <v-card-actions class="justify-center mb-3">
                            <v-btn large class="primary white--text" @click.prevent="register" :loading="isLoading">Register</v-btn>
                        </v-card-actions>
                        <div class="login">
                            <p class="body-2 text-center">
                               Already a member?<router-link to="/login"> Login Now</router-link>
                            </p>
                        </div>
                        <div v-if="createError">
                            <div class="pink lighten-1 red--text lighten-3 pa-4">
                            <div v-for="(err, i) in createErrResponse" :key="i">
                                <div v-for="(msg, j) in err" :key="j">{{ msg.field }} - {{ msg.message }}</div>
                            </div>
                            </div>
                        </div>
                    </v-card>
                </v-col>
                <v-snackbar v-model="createErrorSb" :timeout="5000" top color="red darken-1 white--text">
                    User registeration failed.
                    <v-btn text color="white--text" @click="createErrorSb = false">Close</v-btn>
                </v-snackbar>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            email: '',
            password: '',
            isLoading: false,
            createError: false,
            createErrorSb: false,
            createErrResponse: null,
            createdMsg: [],
            user: {
                f_name: '',
                l_name: '',
                email: '',
                phone: '',
                gender: '',
                location1: '',
                location2: '',
                state: '',
                password: '',
                c_password: ''
            },
            gender: [
                {name: 'Male', value: 'M'},
                {name: 'Female', value: 'F'},
            ],
            checkbox: false,
            agreeToTerms: false,
            agreeValdtn: '',
            api: "http://localhost:8000/api/",
        }
    },
    beforeRouteEnter(to, from, next) {
        next(vm => {
        if (vm.authToken) {
            next("/");
        }
        });
    },
    computed: {
        campaignToBack(){
            return this.$store.getters.campaignToBack
        },
        authToken() {
            return this.$store.getters.getToken;
        },
    },
    methods: {
        capFirst(str){
            return str.charAt(0).toUpperCase() + str.slice(1);
        },
        register(){
            this.$validator.validateAll().then(isValid => {
                if (isValid) {
                    if(this.checkbox == true){
                        console.log(this.user)
                        this.isLoading = true;
                        this.$axios.post(this.api + 'user/register/', {
                            first_name: this.capFirst(this.user.f_name),
                            last_name: this.capFirst(this.user.l_name),
                            email: this.user.email,
                            gender: this.user.gender,
                            phone_no: this.user.phone,
                            location: this.user.location1 + ' ' + this.user.location2 + ' ' + this.user.state,
                            password: this.user.password,
                            c_password: this.user.c_password
                        }).then(res => {
                            this.isLoading = false;
                            console.log(res.data);
                            this.createdMsg = res.message;
                            localStorage.setItem('new_reg', JSON.stringify(res.data.user))
                            this.$router.push({name: 'UploadProfilePhoto'});
                            //send email here
                            // this.sendWelcomeMail(res.data.user)
                        }).catch(err => {
                            this.isLoading = false;
                            this.createError = true;
                            this.createErrorSb = true;
                            this.createErrResponse = err.response.data;
                            console.log(err.response.data);
                        });
                    }else{
                        this.agreeToTerms = true
                        this.agreeValdtn = 'You must agree to our Terms & Policy to register'
                    }
                }
            })
        },
        sendWelcomeMail(user){
            this.$axios.post(this.api + 'send-welcome-mail/', {
                first_name: user.first_name,
                email: user.email,
            }).then((res) => {
                console.log(res.data)
            })
        }
    },
}
</script>

<style lang="scss" scoped>
.v-card {
  .v-card__actions {
    .v-btn {
      width: 50% !important;
    }
  }
  .login{
      padding: 10px;
      margin-bottom: 15px;
      p a {
        text-decoration: none;
    } 
  } 
}
</style>
