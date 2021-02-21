<template>
    <div class="my_donations pt-4">
        <v-card elevation="12" light min-height="200" class="mt-n4">
            <v-card-title class="title justify-center">My Donations<span v-if="myDonations.length > 0">({{ myDonations.length }})</span></v-card-title>
            <v-divider></v-divider>
            <template v-if="isLoading">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
            </template>
            <template v-else>
                <template v-if="myDonations.length == 0">
                    <v-card-text>You have not backed any campaign.</v-card-text>
                </template>
                <template v-else>
                    <v-card-text align="left" class="mt-n5">
                        <v-list three-line nav class="ml-n4 py-4 px-4">
                            <v-list-item-group color="primary" v-for="(donation, i) in myDonations.slice(0, 5)" :key="donation.id">
                                <v-list-item :to="{name: 'CampaignShow', params: {id: donation.project.id, slug: donation.project.slug }}">
                                    <v-list-item-content >
                                        <v-list-item-title class="font-weight-bold primary--text">
                                            {{ donation.project.title | truncate(60)}}
                                        </v-list-item-title>
                                        <v-list-item-subtitle class="mt-2 ml-3">
                                            {{ donation.date }} - <span class="font-weight-bold red--text lighten--2 subtitle-1">&#8358;{{ parseInt(donation.amount) | price }}</span>
                                        </v-list-item-subtitle>
                                        <v-list-item-subtitle class="mt-2 ml-3">
                                            {{ donation.comment }}
                                        </v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                                <v-divider v-if="i < myDonations.length - 1"></v-divider>
                            </v-list-item-group>
                        </v-list>
                    </v-card-text>
                    <v-card-actions v-if="myDonations.length > 5">
                        <v-btn text light class="primary--text" :to="{name: 'ProjectsIBack'}">All Projects I Backed</v-btn>
                    </v-card-actions>
                </template>
            </template>
        </v-card>
    </div>
</template>

<script>
export default {
    data() {
        return {
            myDonations: [],
            isLoading: false,
            api: "http://localhost:8000/api/",
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
        getMyDonations(){
            this.isLoading = true
            this.$axios.get(this.api + 'my-donations/', this.config).then((res) => {
                this.isLoading = false
                // console.log(res.data)
                this.myDonations = res.data
            }).catch(() => {
                this.isLoading = false
            })
        },
    },
    created() {
        this.getMyDonations()
    },
}

</script>