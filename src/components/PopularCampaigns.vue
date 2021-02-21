<template>
      <v-container>
          <v-row wrap justify="start" class="mt-5 mb-5">
              <v-col cols="6" md="2">
                  <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
              </v-col>
          </v-row>
          <v-row wrap class="mt-3 mb-5" justify="end">
              <v-col cols="8">
                  <template v-if="filter_category">
                    <div class="text-center headline">Popular Campaigns: {{ filter_category.name }} Category </div>
                  </template>
                  <template v-else>
                      <div class="text-center headline">Popular Campaigns</div>
                  </template>
              </v-col>
              <v-col cols="4">
                  <div class="mt-n6 px-2">
                      <v-select label="Filter By Category" :items="categories" v-model="filter_category" item-text="name" return-object required persistent-hint name="category" @change="filterByCategory"></v-select>
                  </div>
              </v-col>
          </v-row>
          <v-row wrap justify="start" class="pt-5">
              <v-col cols="12" md="4" class="justify-space-around" v-for="campaign in campaigns.slice(0, 10)" :key="campaign.id">
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
                              <div class="body-2 font-italic ml-3">Expires in {{ campaign.to_expire }} days</div>
                        </v-card-text>
                </v-card>
              </v-col> 
          </v-row>
      </v-container>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
      popular: [],
      api: "http://localhost:8000/api/",
      categories: [],
      filter_category: null,
    }
  },
  methods: {
    getCategories(){
        this.$axios.get(this.api + 'categories/').then((res) => {
            this.categories = res.data
        })
    }, 
    getPopularCampaigns(){
      this.$axios.get(this.api + 'project_list/').then((res) => {
        let favs = res.data.sort((a, b) => parseInt(b.percent_raised - a.percent_raised))
        this.campaigns = favs
        this.popular = favs
      })
    },
    filterByCategory(){
        if(this.filter_category != null){
            let list = this.popular
            let filt = list.filter(a => a.category.id == this.filter_category.id)
            this.campaigns = filt
        }
    },
  },
  created() {
    this.getPopularCampaigns()
    this.getCategories()
    // this.searchCampaign()
  },
}
</script>
    
<style scoped>

</style>
