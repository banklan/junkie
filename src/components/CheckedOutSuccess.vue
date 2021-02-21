<template>
    <div class="checked_out">
        <v-container>
            <v-row wrap justify="center" class="mt-5">
                <v-col cols="12" md="8">
                    <v-alert border="left" type="success">Thank you for backing this campaign, we appreciate your donation and your goodwill message. God bless you.</v-alert>
                    <router-link to="/">
                        <v-btn class="primary white--text mt-3" large rounded elevation="3">Back to Home</v-btn>
                    </router-link>
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
    },
}
</script>