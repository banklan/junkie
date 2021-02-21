<template>
   <div class="home">
     <div class="banner">
        <div class="caption">
          <div class="text-h3 font-weight-regular white--text mt-8 mb-9">Back a campaign, support a startup...</div>
          <div class="text-h4 font-weight-medium secondary--text mb-7">...Help build a dream</div>
          <v-btn x-large rounded class="primary white--text mt-8" to="/create_new">Start A Kolabo</v-btn>
        </div>
     </div>
     <v-progress-circular v-if="loading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
     <template v-else>
        <what-we-do></what-we-do>
        <popular-campaigns :campaigns="popular"></popular-campaigns>
        <featured-campaigns :campaigns="featured"></featured-campaigns>
        <fresh-campaigns></fresh-campaigns>
        <top-categs></top-categs>
        <why-choose></why-choose>
        <success-stories></success-stories>
        <our-partners></our-partners>
     </template>
   </div>
</template>


<script>
export default{
  data(){
    return{
      projects: [],
      api: "http://localhost:8000/api/",
      loading: false,
      popular: [],
      featured: []
    }
  },
  methods: {
    getCampaigns(){
      this.loading = true
      this.$axios.get(this.api + 'project_list/').then((res) => {
        this.loading = false
        this.projects = res.data
        console.log(res.data)

        // filter popular
        let popular = res.data.sort((a, b) => parseFloat(b.percent_raised) - parseFloat(a.percent_raised))
        this.popular = popular

        // this.getFeatured(res.data)
        let featured = res.data.filter(a => a.is_featured === true)
        this.featured = featured
      })
    },
    getFeatured(campaigns){
      let featured = campaigns.filter(a => a.is_featured === true)
      this.featured = featured
      // console.log(featured)
    }
  },
  created(){
    this.getCampaigns()
  }
}
</script>

<style lang="scss" scoped>
    .v-application .title {
        font-size: 1.1rem !important;
        font-weight: 500;
        line-height: 1.7rem;
    }
</style>