<template>
    <div class="registered">
        <v-container>
            <v-row wrap align="center" justify="center">
                <v-col cols="12" md="8">
                    <v-alert type="success" border="left" class="mt-16">
                        Your password has been reset! You can now <router-link to="/login">log in</router-link> with your new password.
                    </v-alert>
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
                next("/");
            }
        });
    },
    computed: {
        authToken(){
            return this.$store.getters.getToken
        }
    },
}
</script>
