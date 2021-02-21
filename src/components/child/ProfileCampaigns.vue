<template>
    <div class="profile_campaign">
        <v-card elevation="12" light min-height="200" class="mb-4 mt-6 px-4">
            <v-card-title class="title justify-center">My Campaigns<span v-if="myCampaigns.length > 0">({{ myCampaigns.length }})</span></v-card-title>
            <v-divider></v-divider>
            <template v-if="isLoading">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
            </template>
            <template v-else>
                <template v-if="myCampaigns.length == 0">
                    <v-card-text>You have not set up any campaigns.</v-card-text>
                </template>
                <template v-else>
                    <v-card-text align="left">
                        <v-list nav three-line class="ml-n4">
                            <v-list-item-group color="primary lighten--2" v-for="(campaign, i) in myCampaigns" :key="campaign.id">
                                <v-list-item :to="{name: 'CampaignShow', params: {id: campaign.id, slug: campaign.slug }}">
                                    <v-list-item-content>
                                        <v-list-item-title class="font-weight-bold primary--text mt-3 ml-2 mb-2.">
                                            {{ campaign.title | truncate(80) | capFirstLetter }}
                                        </v-list-item-title>
                                        <v-list-item-subtitle class="mt-2">
                                            <table class="table table-hover table-striped" v-if="campaign">
                                                <tr>
                                                    <th>Date Published: </th>
                                                    <td>{{ campaign.created }}</td>
                                                </tr>
                                                <tr>
                                                    <th>No of Backers: </th>
                                                    <td>{{  campaign.donations.length }}</td>
                                                </tr>
                                                <tr>
                                                    <th>No Of Followers: </th>
                                                    <td>{{ campaign.followers.length }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Goal: </th>
                                                    <td>&#8358;{{ parseInt(campaign.goal) | price }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Total Donations: </th>
                                                    <td>&#8358;{{ parseInt(campaign.total_donations) | price }}</td>
                                                </tr>
                                                <tr>
                                                    <th>Percentage Raised: </th>
                                                    <td>{{ campaign.percent_raised}}%</td>
                                                </tr>
                                                <tr>
                                                    <th>Expiry: </th>
                                                    <td v-if="campaign.to_expire > 0">{{ campaign.expiry }} - ({{ parseInt(campaign.to_expire) | pluralize('day') }} ) </td>
                                                    <td v-if="campaign.to_expire < 0" class="pink--text darken-3">Expired on {{ campaign.expiry }} - ({{ parseInt(campaign.to_expire * -1) | pluralize('day')}} ago)</td>
                                                    <td v-if="campaign.to_expire == 0">{{ campaign.expiry }} - Expires today</td>
                                                </tr>
                                            </table>
                                        </v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                                <v-card-actions class="justify-center pb-6 mt-5">
                                    <v-btn outlined color="primary" @click="manageMyCampaign(campaign)"><v-icon left>edit</v-icon>Manage Campaign</v-btn>
                                    <v-btn class="secondary white--text" @click="confirmDelete(campaign)"><v-icon left>delete_forever</v-icon>Delete Campaign</v-btn>
                                </v-card-actions>
                                <v-divider v-if="i < myCampaigns.length - 1"></v-divider>
                            </v-list-item-group>
                        </v-list>
                    </v-card-text>
                </template>
            </template>
        </v-card>
        
        <v-card elevation="12" light min-height="200" class="pt-4 mt-4">
            <v-card-title class="title justify-center">Campaigns that i follow<span v-if="myFollows.length > 0">({{ myFollows.length }})</span></v-card-title>
            <v-divider></v-divider>
            <template v-if="isLoading">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
            </template>
            <template v-else>
                <template v-if="myFollows.length == 0">
                    <v-card-text>You have not followed any campaign.</v-card-text>
                </template>
                <template v-else>
                    <v-card-text align="start">
                        <v-list nav class="px-4">
                            <template v-if="!showAllFollows">
                                <v-list-item-group color="primary" v-for="(follow, i) in myFollows.slice(0, 3)" :key="follow.id">
                                    <v-list-item :to="{name: 'CampaignShow', params: {id: follow.project.id, slug: follow.project.slug }}">
                                        <v-list-item-content class="px-3">
                                            <v-list-item-title class="font-weight-bold primary--text">
                                                {{ follow.project.title | truncate(60)}}
                                            </v-list-item-title>
                                            <v-list-item-subtitle class="font-italic">
                                                {{ follow.date }} 
                                            </v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-divider v-if="i < myFollows.length - 1"></v-divider>
                                </v-list-item-group>
                                <v-btn text dark class="my-3 primary--text" v-if="myFollows.length > 3" @click="showAllFollows = true">Show All</v-btn>
                            </template>
                            <template v-else>
                                <v-list-item-group color="primary" v-for="(follow, i) in myFollows" :key="follow.id">
                                    <v-list-item :to="{name: 'CampaignShow', params: {id: follow.project.id, slug: follow.project.slug }}">
                                        <v-list-item-content class="px-3">
                                            <v-list-item-title class="font-weight-bold primary--text">
                                                {{ follow.project.title | truncate(60)}}
                                            </v-list-item-title>
                                            <v-list-item-subtitle class="font-italic">
                                                {{ follow.date }} 
                                            </v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-divider v-if="i < myFollows.length - 1"></v-divider>
                                </v-list-item-group>
                                <v-btn text dark class="my-3 primary--text" @click="showAllFollows = false">Show Less</v-btn>
                            </template>
                        </v-list>
                    </v-card-text>
                </template>
            </template>
        </v-card>
        <v-dialog v-model="confDelDialogue" max-width="450">
            <v-card>
                <v-card-title class="subtitle-1 justify-center">Do you really want to delete this campaign? </v-card-title>
                <v-card-text class="subtitle-2 mt-3 mb-2" align="start">
                    <span>Once deleted, you will not be able to get it back.</span>
                    <v-alert type="warning" border="left" class="mt-4 subtitle-1">Please note that you cannot delete a campaign that has been backed.</v-alert>
                </v-card-text>
                <v-card-actions class="pb-4">
                    <div class="flex-grow-1"></div>
                    <v-btn text dark color="red darken-1" @click="clearDelReq">Cancel </v-btn>
                    <v-btn dark color="primary" @click="deleteCamp" :loading="isDeleting">Yes, Delete </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-snackbar v-model="cantDelCampaign" :time="12000" top color="red darken-2 white--text">You are not allowed to delete a campaign that has already been backed. Kindly contact us. 
            <v-btn text color="white--text" @click="cantDelCampaign = false">Close</v-btn>
        </v-snackbar>
        <v-snackbar v-model="delSuccess" :time="6000" top color="green darken-2 white--text">Your campaign has been deleted. 
            <v-btn text color="white--text" @click="delSuccess = false">Close</v-btn>
        </v-snackbar>
    </div>
</template>


<script>
export default{
    props: ['profile'],
    data(){
        return{
            isLoading: false,
            api: "http://localhost:8000/api/",
            myCampaigns: [],
            myFollows: [],
            showAllFollows: false,
            campaignToDel: null,
            confDelDialogue: false,
            cantDelCampaign: false,
            isDeleting: false,
            delSuccess: false
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
        getMyCampaign(){
            this.isLoading = true
            this.$axios.get(this.api + 'my-projects/', this.config).then((res) => {
                this.isLoading = false
                console.log(res.data)
                this.myCampaigns = res.data
            }).catch(() => {
                this.isLoading = false
            })
        },
        getMyFollows(){
            this.isLoading = true
            this.$axios.get(this.api + 'my-follows/', this.config).then((res) => {
                this.isLoading = false
                console.log(res.data)
                this.myFollows = res.data
            }).catch(() => {
                this.isLoading = false
            })
        },
        confirmDelete(campaign){
            this.campaignToDel = campaign
            this.confDelDialogue = true
        },
        deleteCamp(){
            if(this.campaignToDel.donations.length == 0){
                this.isDeleting = true
                this.$axios.delete(this.api + `delete_project/${this.campaignToDel.id}/`, this.config).then((res) => {
                    this.isDeleting = false
                    this.getMyCampaign()
                    this.delSuccess = true
                    this.clearDelReq()
                    console.log(res.data)
                })
            }else{
                this.cantDelCampaign = true
                this.clearDelReq()
            }
        },
        clearDelReq(){
            this.confDelDialogue = false
            this.campaignToDel = null
        },
        manageMyCampaign(campaign){
            this.$router.push({name: 'ManageMyCampaign', params:{id: campaign.id, slug: campaign.slug}})
        }
    },
    created(){
        this.getMyCampaign()
        this.getMyFollows()
    }
}
</script>


<style scoped lang="scss">
    a{
        text-decoration: none !important;
        font-size: 16px;
        transition: all .4s;
        // &:hover
        &:hover, &:active{
            color: #f3a411;
        } 
    }
</style>