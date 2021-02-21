<template>
    <div class="popular">
        <v-container>
            <v-row wrap justify="center" class="mt-8">
                <div class="text-h4 column-head font-weight-regular mt-8 mb-3">
                    Popular Campaigns
                </div>
            </v-row>
            <v-row wrap align="start" justify="center">
                <v-col cols="12" md="4" v-for="campaign in campaigns.slice(0, 3)" :key="campaign.id">
                    <v-card elevation="12" light min-height="400" class="mx-auto mb-4" :to="{name: 'CampaignShow', params:{id: campaign.id, slug: campaign.slug}}">
                        <v-img :src="campaign.image" height="220" transition="scale-transition" aspect-ratio="1"></v-img>
                        <v-card-title class="card-title justify-center mb-2">{{ campaign.title | truncate(50) | capFirstLetter }}</v-card-title>
                        <v-card-text align="center" class="mt-n5">
                          <v-chip>{{ campaign.category.name }}</v-chip>
                        </v-card-text>
                        <v-card-text class="body-1 mt-1" align="start">
                            <div class="mb-2">Raised <span class="font-weight-bold primary--text">&#8358;{{ parseInt(campaign.total_donations) | price }}</span> of <span class="font-weight-bold primary--text">&#8358;{{ parseInt(campaign.goal) | minPrice }}</span> | {{ campaign.percent_raised }}%</div>
                            <v-progress-linear v-model="campaign.percent_raised" :color="campaign.percent_raised > 50 ? 'green' : 'orange'" height="12"></v-progress-linear>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions class="mx-5 my-3">
                          <v-row align="center" justify="start"> 
                             <div class="body ml-3">By {{ campaign.author.fullname }}</div>
                          </v-row> 
                        </v-card-actions>
                        <v-divider></v-divider>
                        <v-card-text align="start" class="primary white--text">
                              <div class="body-2 font-italic ml-3" v-if="campaign.to_expire > 0">Expires in {{ campaign.to_expire }} days</div>
                              <div class="body-2 font-italic ml-3" v-else>
                                  <span v-if="campaign.to_expire == 0">Expires today</span>
                                  <span v-else>Expired {{ campaign.to_expire  * -1}} days ago</span>
                              </div>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row justify="center" class="mt-5 mb-3">
                <v-btn x-large dark class="secondary" :to="{name: 'PopularCampaigns'}">View Popular Campaigns</v-btn>
            </v-row>
        </v-container>
    </div>
</template>


<script>
export default{
    props: ['campaigns']
}
</script>