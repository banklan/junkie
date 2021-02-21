<template>
   <div class="campaign_show">
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
                       <template v-if="!campaign">
                           <v-alert border="left" type="warning">Campaign does not exist!</v-alert>
                       </template>
                       <template v-else>
                            <v-alert type="warning" border="left" v-if="account && account.status === 404">
                                Kindly <router-link :to="{name: 'BankDetails'}">add your bank details </router-link>to your profile. Your campaign will not be approved and visible until you do so. Thank you.
                            </v-alert>
                            <div class="headline font-weight-medium my-5 pb-4"> {{ campaign.title | capFirstLetter }}</div>
                            <v-card class="mb-4" light outlined min-height="550">
                                <v-img :src="campaign.image" aspect-ratio="1" height="380" transition="scale-transition"></v-img>
                                <v-card-actions class="mx-5 my-3">
                                    <v-row align="center" justify="start"> 
                                        <v-avatar>
                                            <v-img :src="campaign.author.picture" :alt="campaign.author.fullname"></v-img>
                                        </v-avatar>
                                        <div class="body-1 ml-3"><router-link :to="{name: 'MembersPage', params:{id: campaign.author.id, slug: campaign.author.first_name +'-'+ campaign.author.last_name}}">{{ campaign.author.fullname }}</router-link></div>
                                    </v-row> 
                                </v-card-actions>
                                <v-card-text class="body-1 mt-n2" align="start">
                                    <span class="mr-2">Published on {{ campaign.created }}, to expire in {{ campaign.to_expire }} days</span> |
                                    <span class="ml-2">{{ campaign.category.name }}</span> | <v-icon dense color="primary" class="ml-3 mt-n1">visibility</v-icon> {{ campaign.view_count | pluralize('view')}}
                                </v-card-text>
                                <v-card-text class="mt-n2" v-if='!campaign.paid'>
                                    <vue-goodshare-facebook page_url="'http://localhost/campaign/' + campaign.id +'/' + campaign.slug"
                                                        title_social="Facebook" has_counter has_icon></vue-goodshare-facebook>
                                    <vue-goodshare-twitter page_url="'http://localhost/campaign/' + campaign.id +'/' + campaign.slug"
                                                        title_social="Twitter" has_counter has_icon></vue-goodshare-twitter>
                                    
                                </v-card-text>
                                <v-divider></v-divider>
                                <v-card-text class="body-text" align="start">{{ campaign.details |  capFirstLetter}}</v-card-text>
                            </v-card>
                            <v-card class="mb-4" light outlined min-height="350">
                                <v-card-title class="headline justify-center mb-2 primary lighten--2 white--text"> Updates({{ campaign.updates.length }})</v-card-title>
                                <template v-if="campaign.updates.length == 0">
                                    <v-card-text align="start" class="body-1">There are no updates for this campaign.</v-card-text>
                                </template>
                                <template v-else>
                                    <template v-if="campaign.updates.length > 3">
                                        <template v-if="!showAllUpdates">
                                            <div v-for="(update, i) in campaign.updates.slice(0, 3)" :key="i" class="py-3 px-3">
                                                <v-img :src="update.image" aspect-ratio="1" height="250" transition="scale-transition"></v-img>
                                                <v-card-title class="justify-center title"> {{ update.title }}</v-card-title>
                                                <v-card-text align="start" class="body-1">{{ update.details | truncate(200) }}</v-card-text>
                                                <v-card-actions class="body-2 font-italic">- {{ update.date }}</v-card-actions>
                                                <v-divider v-if="i < campaign.updates.length - 1"></v-divider>
                                            </div>
                                            <v-card-actions class="justify-center">
                                                <v-btn text color="primary" @click="showAllUpdates = true">All Updates</v-btn>
                                            </v-card-actions>
                                        </template>
                                        <template v-else>
                                            <div v-for="(update, i) in campaign.updates" :key="i" class="py-3 px-3">
                                                <v-img :src="update.image" aspect-ratio="1" height="250" transition="scale-transition"></v-img>
                                                <v-card-title class="justify-center title"> {{ update.title }}</v-card-title>
                                                <v-card-text align="start" class="body-1">{{ update.details | truncate(200) }}</v-card-text>
                                                <v-card-actions class="body-2 font-italic">- {{ update.date }}</v-card-actions>
                                                <v-divider v-if="i < campaign.updates.length - 1"></v-divider>
                                            </div>
                                            <v-card-actions class="justify-center">
                                                <v-btn text color="primary" @click="showAllUpdates = false">Less Updates</v-btn>
                                            </v-card-actions>
                                        </template>
                                    </template>
                                    <template v-else>
                                        <div v-for="(update, i) in campaign.updates" :key="i" class="pt-3 px-3">
                                            <v-img :src="update.image" aspect-ratio="1" height="250" transition="scale-transition"></v-img>
                                            <v-card-title class="justify-center title"> {{ update.title }}</v-card-title>
                                            <v-card-text align="start" class="body-1">{{ update.details | truncate(200) }}</v-card-text>
                                            <v-card-actions class="body-2 font-italic">- {{ update.date }}</v-card-actions>
                                            <v-divider v-if="i < campaign.updates.length - 1"></v-divider>
                                        </div>
                                    </template>
                                </template>
                            </v-card>
                       </template>
                   </template>
               </v-col>
               <v-col cols="12" md="4">
                   <v-card light elevation="6" min-height="350" class="sidelounge" v-if="campaign">
                       <v-card-text>
                            <div class="mb-2 mt-5">
                                <span class="title primary--text">&#8358;{{ parseInt(campaign && campaign.total_donations) | price }}</span> raised ({{ campaign && campaign.percent_raised }}%)
                            </div>
                            <v-progress-linear v-model="campaign.percent_raised" :color="campaign.percent_raised > 50 ? 'green' : 'orange'" height="12"></v-progress-linear>
                            <div class="title body-text mt-4 secondary--text darken-3" align="start">
                                Goal: &#8358;{{ parseInt(campaign.goal) | price }}
                            </div>
                            <div class="subtitle-2 mt-3" align="start">
                                <span class="mr-1">
                                    <router-link :to="{name: 'CampaignBackers', params: {id: campaign.id, slug: this.campaign.slug}}">{{ campaign.donations.length | pluralize('Backer') }}</router-link></span> 
                                    | <span v-if="!isLoggedIn">{{ followCounts | pluralize('follower') }}</span> <span v-if="isLoggedIn"><v-btn text color="primary--text" @click.prevent="showFollowers = true">{{ followCounts | pluralize('follower') }} </v-btn></span> 
                                    | <span>{{ campaign.to_expire | pluralize('day')}} to go</span>
                            </div>
                       </v-card-text>
                       <v-card-text v-if="!isMine">
                            <template v-if="!campaign.paid">
                                <v-btn color="primary white--text" large block @click.prevent="backCampaign">Back Campaign</v-btn>
                                <v-btn v-if="canFollow" color="secondary white--text" class="mt-3" large block @click.prevent="followCampaign" :loading="isFollowing">Follow this Campaign</v-btn>
                            </template>
                            <template v-else>
                                <v-btn disabled large>Campaign Completed</v-btn>
                            </template>
                       </v-card-text>
                       <v-divider class="mt-5"></v-divider>
                       <v-card-text>
                           <template v-if="campaign.donations && campaign.donations.length > 0">
                                <div class="subtitle-1 body-text mb-3">{{ campaign.donations.length | pluralize('backer') }} have donated to this campaign.</div>
                                <v-list rounded class="ml-n4">
                                    <v-list-item-group class="mb-3" color="primary lighten--2" v-for="(donation, i) in campaign.donations.slice(0, 3)" :key="donation.id">
                                        <v-list-item>
                                            <v-list-item-avatar>
                                                <v-img v-if="donation.backer != 'Anonymous'" :src="donation.name.picture" :alt="donation.name.fullname"></v-img>
                                                <v-img v-else src="../assets/images/no_image.jpg" :alt="donation.name.fullname"></v-img>
                                            </v-list-item-avatar>
                                            <v-list-item-content>
                                                <v-list-item-title>{{ donation.backer }}</v-list-item-title>
                                                <v-list-item-title>{{ donation.date }}</v-list-item-title>
                                            </v-list-item-content>
                                            <v-list-item-content>
                                                <v-list-item-title color="primary--text">&#8358;{{ parseInt(donation.amount) | price }}</v-list-item-title>
                                            </v-list-item-content>
                                        </v-list-item>
                                        <span v-if="campaign.donations.length > 3">
                                            <v-divider class="mt-5 mb-5" v-if="i < 3"></v-divider>
                                        </span>
                                        <span v-else>
                                            <v-divider class="mt-5 mb-5" v-if="i < campaign.donations.length - 1"></v-divider>
                                        </span>
                                    </v-list-item-group>
                                    <router-link v-if="campaign && campaign.donations.length > 3" :to="{name: 'CampaignBackers', params: {id: campaign.id, slug: this.campaign.slug}}">See All Backers</router-link>
                                </v-list>
                            </template>
                            <template v-else>
                                There are no backers for this campaign yet.
                            </template>
                       </v-card-text>
                   </v-card>
                   <v-card light elevation="6" min-height="250" class="sidelounge" v-if="campaign">
                       <v-card-title class="headline justify-center mb-2 primary lighten--2 white--text">Campaigns Like This</v-card-title>
                       <template v-if="relatedCampaigns.length < 1">
                           <v-card-text class="body-1">
                                There are no related campaigns
                           </v-card-text>
                       </template>
                       <template v-else>
                           <v-card-text>
                               <v-list three-line nav>
                                    <v-list-item-group color="primary lighten--2" v-for="(item, index) in relatedCampaigns.slice(0, 3)" :key="item.id">
                                        <v-list-item :to="{name: 'CampaignShow', params: {id: item.id, slug:item.slug}}" :key="item.title" class="mt-3" link>
                                            <v-list-item-avatar>
                                                <v-img :src="item.image" height="250" alt="campaign Image"></v-img>
                                            </v-list-item-avatar>
                                            <v-list-item-content class='mt-n3'>
                                                <v-list-item-title class="subtitle-1 primary--text">{{ item.title | capFirstLetter }}</v-list-item-title>
                                                <v-list-item-subtitle class="mt-n3 subtitle-2">{{ item.created }}</v-list-item-subtitle>
                                            </v-list-item-content>
                                        </v-list-item>
                                        <v-divider v-if="index < 2"></v-divider>
                                    </v-list-item-group>   
                                </v-list>
                            </v-card-text>
                       </template>
                   </v-card>
               </v-col>
           </v-row>
           <v-dialog v-model="showFollowers" max-width="400">
                <v-card>
                    <v-card-title class="title justify-center">Followers of this campaign</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="subtitle-1" align="start">
                        <template v-if="campaign">
                            <template v-if="campaign.followers.length > 0">
                                <div v-for="follower in campaign.followers" :key="follower.id">
                                    <div class="my-2">
                                        <router-link :to="{name: 'MembersPage', params: { id: follower.follower.id, slug:follower.follower.first_name + '-' + follower.follower.last_name }}">{{ follower.follower.fullname }}</router-link>
                                    </div>
                                    <v-divider></v-divider>
                                </div>
                            </template>
                            <template v-else>
                                <div class="mt-4">
                                    This campaign has no followers yet.
                                </div>
                            </template>
                        </template>
                    </v-card-text>
                    <v-card-actions>
                        <div class="flex-grow-1"></div>
                        <v-btn text dark color="red darken-1" @click="showFollowers = false"> Got It! </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-snackbar v-model="cannotBackYourCampaign" :time="5000" top color="red darken-2 white--text">You cannot back your own campaign. 
                <v-btn text color="white--text" @click="cannotBackYourCampaign = false">Close</v-btn>
            </v-snackbar>
       </v-container>
   </div>
</template>

<script>
import VueGoodShareFacebook from 'vue-goodshare/src/providers/Facebook.vue'
import VueGoodShareTwitter from 'vue-goodshare/src/providers/Twitter.vue'
// import VueGoodShareInstagram from 'vue-goodshare/src/providers/Instagram.vue'

export default {
    components: {
        'vue-goodshare-facebook': VueGoodShareFacebook,
        'vue-goodshare-twitter': VueGoodShareTwitter,
        // 'vue-goodshare-instagram': VueGoodShareInstagram,
    },
    data(){
        return{
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            campaign: null,
            api: "http://localhost:8000/api/",
            isLoading: false,
            showAllUpdates: false,
            relatedCampaigns: [],
            showFollowers: false,
            cannotBackYourCampaign: false,
            campaignIsMine: false,
            account: null,
            author: null,
            followers: [],
            canFollow: false,
            followCounts: null,
            isFollowing: false
        }
    },
    watch: {
        $route(){
            this.id = this.$route.params.id
            this.getCampaign()
        }
    },
    computed: {
      getAuth(){
          return this.$store.getters.getAuthUser
      },
      isLoggedIn(){
          return this.$store.getters.isLoggedIn
      },
      authToken(){
          return this.$store.getters.getToken
      },
      isMine(){
        return this.$store.getters.campaignIsMine
      },
      config() {
        let conf = {
            headers: {
                Authorization: "Token " + this.authToken,
            },
        };
        return conf;
      },
      campaignToBack(){
          return this.$store.getters.campaignToBack
      },
      getFollowers(){
          return this.$store.getters.getFollowers
      }
    },
    methods:{
        getCampaign(){
            this.isLoading = true
            this.$axios.get(this.api + `projects/${this.id}/`).then((res) =>{
                this.isLoading = false
                this.campaign = res.data
                // let followers = res.data.followers
                this.followers = res.data.followers
                this.followCounts = res.data.followers.length
                let author = res.data.author
                let auth = this.getAuth.id
                console.log(res.data)

                this.$store.commit("store_campaign", res.data);
                
                //check linked bank account if auth and own campaign
                if(this.isLoggedIn === true){
                    if(author.id == auth){
                        // console.log('this is mine')
                        this.campaignIsMine = true
                        this.$axios.get(this.api + 'check-linked-account/', this.config).then((res) => {
                            console.log(res.data)
                            this.account = res.data
                        })
                    }
                }
                
                //check if i can follow campaign
                // to follow, i must be logged in, campaign must not be mine and i havent followed b4
                    if(this.isLoggedIn === true && author.id !== auth){
                        if(res.data.followers.length > 0){
                            let follws  = []
                            res.data.followers.forEach((foll) => {
                                follws.push(foll.follower.id)
                            })
                            if(follws.indexOf(auth) == -1){
                                this.canFollow = true
                            }else{
                                this.canFollow = false
                            }
                        }else{
                            this.canFollow = true
                        }
                    }

                    // }
                    // console.log(followers.indexOf(auth))
                // }
                
                //campaigns in same category
                this.$axios.get(this.api + `same_categ/${res.data.category.id}/`).then((res) => {
                    this.isLoading = false
                    // console.log(res.data)
                    let related = res.data.filter(a => a.id != this.id)
                    this.relatedCampaigns = related
                }).catch(() => {
                    this.isLoading = false
                })

            }).catch(() => {
                this.isLoading = false
            })
        },
        backCampaign(){
            if(this.isLoggedIn){
                if(this.isMine){
                    this.cannotBackYourCampaign = true
                }else{
                    this.$router.push({name: 'BackCampaign', params: {id: this.campaign.id, slug: this.campaign.slug}})
                }
            }else{
                // commit project to store
                this.$store.commit("campaign_to_back", this.campaign);
                this.$router.push('/login')
            }
        },
        followCampaign(){
            if(this.isMine == false){
                this.isFollowing = true
                this.$axios.post(this.api + `follow-campaign/${this.$route.params.id}/`, {
                    project: this.campaign
                },this.config).then((res) => {
                    this.isFollowing =  false
                    console.log(res.data)
                    // this.campaign.followers.push(this.getAuth)
                    setInterval(() => {
                        this.canFollow = false
                    }, 100)
                    this.followCounts++
                }).catch(() => {
                    this.isFollowing = false
                })
            }
        }
    },
    created() {
        this.getCampaign()
        // console.log(this.isMine)
    },
}
</script>

<style scoped lang="scss">
    @media screen and (min-width: 960px){
        .sidelounge{
            margin-top: 4.5rem !important;
        }
    }
    @media screen and (max-width: 959px){
        .v-avatar.v-list-item__avatar{
            margin-right: -2rem !important;
        }
    }
    a{
        text-decoration: none !important;
        font-size: 16px;
        transition: all .4s;
        &:hover, &:active{
            color: #f3a411;
        }
    }
</style>