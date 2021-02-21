<template>
  <div class="campaigns_cat">
      <v-container>
          <v-row wrap justify="start">
              <v-col cols="6" md="2">
                  <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
              </v-col>
          </v-row>
          <v-row wrap class="mt-3 mb-5" justify="start">
              <v-col cols="8">
                  <div class="text-center headline" v-if="category">Category: {{ category.name }} </div>
              </v-col>
              <v-col cols="3">
                  <div class="mt-n6 mr-n5">
                      <v-select label="Change Category" :items="categories" v-model="new_category" item-text="name" return-object required persistent-hint v-validate="'required'" :error-messages="errors.collect('category')" name="category" @change="changeCategory"></v-select>
                  </div>
              </v-col>
            </v-row> 
            <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
            <template v-else>
                <template v-if="campaigns.length == 0">
                    <v-row wrap justify="center" class="mt-4">
                        <v-col cols="12" md="6" class="justify-center">
                            <v-alert type="info" border="left">
                                There are no campaigns for this category.
                            </v-alert>
                        </v-col>
                    </v-row>
                </template>
                <template v-else>
                    <v-row wrap justify="start" class="mt-4">
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
                </template>
            </template>
          <v-row justify="end" class="mt-3 pb-4" v-if="campaigns.length != 0">
            <v-col cols="12">
                <div class="text-center">
                    <v-btn :disabled="!previous" color="primary white--text" class="mr-3" link @click="getPrevious"><v-icon left>arrow_left</v-icon>Previous</v-btn>
                    <v-btn :disabled="!next" color="primary white--text" link @click="getNext">Next<v-icon right>arrow_right</v-icon></v-btn>
                </div>
            </v-col>
          </v-row>
      </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
    //   id: this.$route.params.id,
      slug: this.$route.params.slug,
      campaigns: [],
      api: "http://localhost:8000/api/",
      isLoading: false,
      count: null,
      next: null,
      previous: null,
      category: null,
      categories: [],
      new_category: null
    }
  },
  watch: {
      slug(){
          this.getCampaigns()
      }
  },
  methods: {
    getCampaigns(){
      this.isLoading = true
      this.$axios.get(this.api + `projects_by_cat/${this.slug}/`).then((res) => {
          this.isLoading = false
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
          this.$router.push({path: `/campaigns/${this.slug}`, query:{page: pageNum}})
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
                this.$router.push({path: `/campaigns/${this.slug}`})
            }else{
                this.$router.push({path: `/campaigns/${this.slug}`, query:{page: pageNum}})
            }
        })
    },
    getCatName(){
       this.isLoading = true
       this.$axios.get(this.api + `get_cat_name/${this.slug}/`).then((res) => {
         this.isLoading = false
         this.category = res.data
       })
    },
    getCategories(){
        this.$axios.get(this.api + 'categories/').then((res) => {
            this.categories = res.data
        })
    },
    changeCategory(){
        this.category = this.new_category
        this.id = this.new_category.id
        this.slug = this.new_category.slug
        this.$router.push({name: 'CampaignsByCat', params: {slug: this.new_category.slug}})
    }
  },
  created() {
    this.getCatName()
    this.getCampaigns()
    this.getCategories()
  },
}
</script>
    
<style scoped>

</style>
