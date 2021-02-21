<template>
      <v-container>
          <v-row wrap justify="start" class="mt-5 mb-5">
              <v-col cols="6" md="2">
                  <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
              </v-col>
          </v-row>
          <v-row wrap class="mt-3 mb-5" justify="center">
              <v-col cols="12" md="8">
                  <template>
                    <div class="text-center title">Search for "<strong>{{ q }}</strong>" returned {{campaigns.length}} results.</div>
                  </template>
              </v-col>
          </v-row>
          <template v-if="count === 0">
              <v-row wrap justify="center" class="pt-5">
                  <v-alert border="left" type="info">
                      No campaign was found for <strong>{{ q }}</strong>
                  </v-alert>
              </v-row>
          </template>
          <template v-else>
              <v-row wrap justify="start" class="pt-4">
                  <v-col cols="12" md="4" class="justify-space-around" v-for="campaign in campaigns" :key="campaign.id">
                      <v-card elevation="12" light min-height="400" class="mx-auto mb-4" :to="{name: 'CampaignShow', params:{id: campaign.id, slug: campaign.slug}}">
                        <v-img :src="campaign.image" height="220" transition="scale-transition" aspect-ratio="1"></v-img>
                        <v-card-title class="title justify-center mb-2">{{ campaign.title | truncate(120) }}</v-card-title>
                        <v-card-text align="center" class="mt-n5">
                          <v-chip>{{ campaign.category.name }}</v-chip>
                        </v-card-text>
                        <v-card-text class="body-1 mt-1" align="start">
                            <div class="mb-2">Raised <span class="font-weight-bold primary--text">&#8358;{{ parseInt(campaign.total_donations) | price }}</span> of <span class="font-weight-bold primary--text">&#8358;{{ parseInt(campaign.goal) | price }}</span></div>
                            <v-progress-linear v-model="campaign.percent_raised" :color="campaign.percent_raised > 50 ? 'green' : 'orange'" height="12"></v-progress-linear>
                        </v-card-text>
                        <v-divider></v-divider>
                        <v-card-actions class="mx-5 my-3">
                          <v-row align="center" justify="start"> 
                                <v-avatar>
                                      <v-img :src="campaign.author.picture" :alt="campaign.author.fullname"></v-img>
                                  </v-avatar>
                                <div class="body ml-3">{{ campaign.author.fullname }}</div>
                          </v-row> 
                        </v-card-actions>
                        <v-divider></v-divider>
                        <v-card-text align="start" class="primary white--text">
                              <div v-if="campaign.to_expire == 0" class="body-2 font-italic ml-3">Expires Today</div>
                              <div v-if="campaign.to_expire > 0" class="body-2 font-italic ml-3">Expires in {{ campaign.to_expire | pluralize('day') }}</div>
                              <div v-if="campaign.to_expire < 0" class="body-2 font-italic ml-3">Expired {{ parseInt(campaign.to_expire * -1) | pluralize('day') }} ago</div>
                        </v-card-text>
                    </v-card>
                  </v-col>
              </v-row>
          </template>
      </v-container>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
      api: "http://localhost:8000/api/",
      q: this.$route.query.q,
      isLoading: false,
      count: 0
    }
  },
  watch: {
      $route(){
        this.q = this.$route.query.q
        this.search()
      }
  },
  methods: {
    search(){
      if(this.$route.query.q){
          this.isLoading = true
          let q = this.$route.query.q
          this.$axios.get(this.api + `search_for_projects?search=${q}`).then((res) => {
              this.isLoading = false
              console.log(res.data)
              this.campaigns = res.data
              this.count = res.data.count
              this.next = res.data.next
              this.previous = res.data.previous
          })
        }
    },
  },
  created() {
    this.search()
  },
}
</script>
