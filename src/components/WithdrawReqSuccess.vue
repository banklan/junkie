<template>
    <div class="withdraw_success">
        <v-container>
            <v-row wrap justify="center" class="mt-10">
                <v-col cols="12" md="9">
                    <v-alert type="success" class="mb-5 pt-5">
                        Your fund withdrawal request has been lodged. We will attend to your request and get back to you within the next 24hours. Thank you
                    </v-alert>
                    <div class="pt-5">
                        <v-btn text large color="primary" to="/profile">Go Back To Profile</v-btn>
                    </div>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    beforeRouteEnter(to, from, next) {
        next(vm => {
            if (vm.authToken) {
                next();
            }else{
                next('/')
            }
        });
    },
    computed: {
        authToken() {
            return this.$store.getters.getToken;
        },
    }
}
</script>