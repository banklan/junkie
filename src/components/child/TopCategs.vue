<template>
    <div class="top_categs">
       <v-container>
           <v-row wrap justify="center" class="mt-8">
               <div class="text-h4 column-head font-weight-regular mt-8 mb-3">
                    Browse By Categories
                </div>
           </v-row>
           <v-row wrap justify="start" class="mt-8" align="center">
                <template v-if="isLoading">
                    <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                </template>
                <template v-else>
                    <v-col cols="6" md="3" v-for="cat in categs" :key="cat.id">
                        <v-btn x-large class="primary white--text" width="60%" :loading="isLoading" :to="{name: 'CampaignsByCat', params: {slug: cat.slug}}">{{ cat.name }}</v-btn>
                    </v-col>
                </template>
           </v-row>
       </v-container> 
    </div>
</template>


<script>
export default {
    data() {
        return {
            categs: [],
            api: "http://localhost:8000/api/",
            isLoading: false,
        }
    },
    methods: {
        getCategs(){
            this.isLoading = true
            this.$axios.get(this.api + 'categories/').then((res) => {
                this.isLoading = false
                this.categs = res.data
                console.log(res.data)
            })
        },
        // browseByCat(cat){
        //     this.isLoading = true
        //     // console.log(cat)
        //     this.$axios.get(this.api + `projects_by_cat/${cat}/`).then((res) => {
        //         this.isLoading = false
        //         console.log(res.data)
        //     })
        // }
    },
    created() {
        this.getCategs()
    },
   
}
</script>


<style lang="scss" scoped>
    
</style>