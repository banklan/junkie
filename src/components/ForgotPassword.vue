<template>
    <div class='forgotten_password'>
        <v-container>
            <v-row wrap align="center" justify="center">
                <v-col cols="12" md="6" v-if="!passwordRequestMail">
                    <v-card elevation="12" light flat min-height="250">
                        <v-card-title class="primary white--text justify-center mt-6">Password Recovery</v-card-title>
                        <v-card-text class="mt-5">
                            <v-text-field label="Input Your Email" v-model="email" required v-validate="'required|email'" :error-messages="errors.collect('email')" name="email"></v-text-field>
                        </v-card-text>
                        <v-card-actions class='justify-center'>
                            <v-btn dark large width="50%" class="primary white--text" :loading="isLoading" @click="sendEmail">Send Email</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <v-col cols="12" md="10" v-else>
                    <v-alert type="success" class="mt-6" border="left">
                        An email has been sent to your email <span class="yellow--text darken-2"><strong>{{ email }}</strong></span>. Kindly follow the instructions contained. Thank you for using junkies.com
                    </v-alert>
                </v-col>
            </v-row>
            <v-snackbar v-model="passwordRequestFailed" :time="12000" top color="red darken-2 white--text">
                Password reset request failed. Please use an email registered on our website and ensure you have a good network connection.
                <v-btn text color="white--text" @click="passwordRequestFailed = false">Close</v-btn>
            </v-snackbar>
        </v-container>
        
    </div>
</template>

<script>
export default {
    data() {
        return {
            email: '',
            isLoading:false,
            api: 'http://localhost:8000/',
            passwordRequestFailed: false,
            passwordRequestMail: false,
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
        authToken(){
            return this.$store.getters.getToken
        }
    },
    methods: {
        sendEmail(){
            this.$validator.validateAll().then(isValid => {
                if (isValid) {
                    this.isLoading = true;
                    this.$axios.post(this.api + 'api/request_password_reset/', {
                            email: this.email
                        }).then(() => {
                            this.isLoading = false
                            this.passwordRequestMail = true
                        }).catch(() => {
                            this.isLoading = false
                            this.passwordRequestFailed = true
                        })
                }
            })
        }
    },
}
</script>