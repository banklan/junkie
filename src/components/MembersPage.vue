<template>
    <div class="members_page">
        <v-container>
            <v-row wrap justify="start">
                <v-col cols="6" md="2">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
                </v-col>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="8">
                   <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                   <template v-else>
                       <template v-if="!user">
                           <v-alert border="left" type="warning">This user does not exist!</v-alert>
                       </template>
                       <template v-else>
                           <v-card elevation="12" light min-height="500" class="pb-5">
                                <v-card-title dark class="primary white--text title justify-center mb-3">{{ user && user.fullname }} Page</v-card-title>
                                <v-img :src="user.picture" height="350" contain transition="scale-transition" aspect-ratio="1" alt="Member's Picture"></v-img>
                                <v-card-text align="center" justify="center" class="ml-4">
                                    <table class="table table-hover table-striped">
                                        <tr>
                                            <th>Name</th>
                                            <td>{{ user.fullname }}</td>
                                        </tr>
                                        <tr>
                                            <th>Email</th>
                                            <td>{{ user.email }}</td>
                                        </tr>
                                        <tr>
                                            <th>Phone Number:</th>
                                            <td>{{ user.phone_no }}</td>
                                        </tr>
                                        <tr>
                                            <th>Location</th>
                                            <td>{{ user.location }}</td>
                                        </tr>
                                    </table>
                                </v-card-text>
                            </v-card>
                       </template>
                   </template>
                </v-col>
                <v-col cols="12" md="4">
                    <v-card elevation="12" light min-height="200" class="pb-5">
                        <template v-if="user">
                            <v-card-title class="justify-center title primary white--text">{{ user.fullname }}'s campaign(s)</v-card-title>
                            <v-card-text>
                                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                                <template v-else>
                                    <template v-if="!userCampaigns">
                                        <div class="warning--text darken-3 subtitle-1 mt-3" align="start">
                                            This user has not started any campaign.
                                        </div>
                                    </template>
                                    <template v-else>
                                        <v-list three-line nav>
                                            <template v-if="!showAllList">
                                                <v-list-item-group color="primary lighten--2" v-for="item in userCampaigns.slice(0, 3)" :key="item.id" align="start">
                                                    <v-list-item :to="{name: 'CampaignShow', params: {id: item.id, slug:item.slug}}" :key="item.title" class="mt-3" link>
                                                        <v-list-item-avatar>
                                                            <v-img :src="item.image" height="250" alt="campaign Image"></v-img>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content class='mt-n3'>
                                                            <v-list-item-title class="subtitle-1 primary--text">{{ item.title | capFirstLetter }}</v-list-item-title>
                                                            <v-list-item-subtitle class="mt-n3 subtitle-2">{{ item.created }}</v-list-item-subtitle>
                                                        </v-list-item-content>
                                                    </v-list-item>
                                                    <v-divider></v-divider>
                                                </v-list-item-group>   
                                                <v-btn v-if="userCampaigns.length > 3" text class="justify-center" color="primary" @click="showAllList = true">Show More</v-btn>
                                            </template>
                                            <template v-else>
                                                <v-list-item-group color="primary lighten--2" v-for="item in userCampaigns" :key="item.id" align="start">
                                                    <v-list-item :to="{name: 'CampaignShow', params: {id: item.id, slug:item.slug}}" :key="item.title" class="mt-3" link>
                                                        <v-list-item-avatar>
                                                            <v-img :src="item.image" height="250" alt="campaign Image"></v-img>
                                                        </v-list-item-avatar>
                                                        <v-list-item-content class='mt-n3'>
                                                            <v-list-item-title class="subtitle-1 primary--text">{{ item.title | capFirstLetter }}</v-list-item-title>
                                                            <v-list-item-subtitle class="mt-n3 subtitle-2">{{ item.created }}</v-list-item-subtitle>
                                                        </v-list-item-content>
                                                    </v-list-item>
                                                    <v-divider></v-divider>
                                                </v-list-item-group>   
                                                <v-btn text class="justify-center" color="primary" @click="showAllList = false">Show Less</v-btn>
                                            </template>
                                        </v-list>
                                    </template>
                                </template>                                
                            </v-card-text>
                        </template>
                        <template v-else>
                            <v-card-text align="start">
                                <div class="warning--text subtitle-1 mt-3" align="start">This user does not exist</div>
                            </v-card-text>
                        </template>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default{
    data() {
        return {
            id: this.$route.params.id,
            user: null,
            isLoading: false,
            api: "http://localhost:8000/api/",
            userCampaigns: null,
            showAllList: false
        }
    },
    methods: {
        getUser(){
            this.isLoading = true
            this.$axios.get(this.api + `members_profile/${this.id}/`).then((res) => {
                this.isLoading = false
                this.user = res.data
                // console.log(res.data)
            })
        },
        getUserCampaigns(){
            this.isLoading = true
            this.$axios.get(this.api + `user_campaigns/${this.id}`).then((res) => {
                this.isLoading = false
                this.userCampaigns = res.data
                console.log(res.data)
            })
        }
    },
    created(){
        this.getUser()
        this.getUserCampaigns()
    }
}
</script>