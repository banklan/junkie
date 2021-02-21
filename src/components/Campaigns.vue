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
                    <div class="text-center headline">Category: {{ filter_category.name }} </div>
                  </template>
                  <template v-else>
                      <div class="text-center headline">All Campaigns</div>
                  </template>
              </v-col>
              <v-col cols="4">
                  <div class="mt-n6 px-2">
                      <v-select label="Filter By Category" :items="categories" v-model="filter_category" item-text="name" return-object required persistent-hint name="category" @change="filterByCategory"></v-select>
                  </div>
              </v-col>
          </v-row>
          <v-row wrap justify="start" class="pt-5">
              <v-col cols="12" md="4" class="justify-space-around" v-for="campaign in campaigns" :key="campaign.id">
                  <v-card elevation="12" light min-height="550" class="mx-auto mb-4" :to="{name: 'CampaignShow', params:{id: campaign.id, slug: campaign.slug}}">
                     <v-img :src="campaign.image" height="250" transition="scale-transition" aspect-ratio="1"></v-img>
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
          <v-row justify="end" class="mt-3 pb-4" v-if="campaigns.length != 0">
            <v-col cols="12">
                <div class="text-center">
                    <v-btn :disabled="!previous" color="primary white--text" class="mr-3" link @click="getPrevious"><v-icon left>arrow_left</v-icon>Previous</v-btn>
                    <v-btn :disabled="!next" color="primary white--text" link @click="getNext">Next<v-icon right>arrow_right</v-icon></v-btn>
                </div>
            </v-col>
          </v-row>
      </v-container>
  <!-- </div> -->
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
      api: "http://localhost:8000/api/",
      count: null,
      next: null,
      previous: null,
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
    getProjects(){
      this.$axios.get(this.api + 'projects/').then((res) => {
        this.campaigns = res.data.results
        this.count = res.data.count
        this.next = res.data.next
        this.previous = res.data.previous
        console.log(res.data)
      })
    },
    getNext(){
      const params = new URL(this.next).searchParams;
      this.$axios.get(this.next).then((res) => {
          this.campaigns = res.data.results
          this.count = res.data.count
          this.next = res.data.next
          this.previous = res.data.previous
          let pageNum = params.get('page')
          this.$router.push({path: `/campaigns`, query:{page: pageNum}})
      })
    },
    getPrevious(){
        const params = new URL(this.previous).searchParams;
        this.$axios.get(this.previous).then((res) => {
            this.campaigns = res.data.results
            this.count = res.data.count
            this.next = res.data.next
            this.previous = res.data.previous
            let pageNum = params.get('page')
            if(pageNum == null){
                this.$router.push({path: `/campaigns`})
            }else{
                this.$router.push({path: `/campaigns`, query:{page: pageNum}})
            }
        })
    },
    filterByCategory(){
        if(this.filter_category != null){
          this.$router.push({name: 'CampaignsByCat', params: {id: this.filter_category.id, slug: this.filter_category.slug}})
        }
    },
  },
  created() {
    this.getProjects()
    this.getCategories()
    // this.searchCampaign()
  },
}
</script>
    
<style scoped>

</style>
