<template>
    <div class="backers">
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
                       <div class="headline font-weight-bold my-5"> {{ campaign.title | capFirstLetter }}</div>
                        <template v-if="backers.length == 0">
                            <v-alert border="left" type="info" class="my-5">We need to put in more effort. We don't have backers for this project yet!</v-alert>
                        </template>
                        <template v-else>
                            <v-card outline light min-height="200" class="mt-5">
                                <template v-if="!showAllBackers">
                                    <div v-for="(backer, i) in backers.slice(0, 10)" :key="backer.id">
                                        <v-card-actions class="mx-5 my-3">
                                            <v-row align="center" justify="start"> 
                                                <v-avatar>
                                                    <v-img v-if="backer.backer === 'Anonymous'" src="@/assets/images/no_image.jpg" :alt="backer.backer"></v-img>
                                                    <v-img v-else :src="backer.name.picture" :alt="backer.name.fullname"></v-img>
                                                </v-avatar>
                                                <div class="body-1 ml-3">{{ backer.backer }} - <span class="font-weight-bold primary--text">&#8358;{{ parseInt(backer.amount) | price }}</span></div>
                                            </v-row> 
                                        </v-card-actions>
                                        <v-card-text align="left" class="mt-n4 body-text"> {{ backer.comment | capFirstLetter }}</v-card-text>
                                        <v-card-text align="left" class="font-italic mt-n5">{{ backer.date }}</v-card-text>
                                        <v-divider v-if="i < backers.length - 1"></v-divider>
                                    </div>
                                    <template v-if="backers.length > 10">
                                        <v-card-actions>
                                            <v-btn text color="primary" @click="showAllBackers = true">View All</v-btn>
                                        </v-card-actions>
                                    </template>
                                </template>
                                <template v-else>
                                    <div v-for="(backer, i) in backers" :key="backer.id">
                                        <v-card-actions class="mx-5 my-3">
                                            <v-row align="center" justify="start"> 
                                                <v-avatar>
                                                    <v-img v-if="backer.backer === 'Anonymous'" src="@/assets/images/no_image.jpg" :alt="backer.backer"></v-img>
                                                    <v-img v-else :src="backer.name.picture" :alt="backer.name.fullname"></v-img>
                                                </v-avatar>
                                                <div class="body-1 ml-3">{{ backer.backer }} - <span class="font-weight-bold">&#8358;{{ parseInt(backer.amount) | price }}</span></div>
                                            </v-row> 
                                        </v-card-actions>
                                        <v-card-text align="left" class="mt-n4 body-text"> {{ backer.comment | capFirstLetter }}</v-card-text>
                                        <v-card-text align="left" class="font-italic mt-n5">{{ backer.date }}</v-card-text>
                                        <v-divider v-if="i < backers.length - 1"></v-divider>
                                    </div>
                                    <template v-if="backers.length > 10">
                                        <v-card-actions>
                                            <v-btn text color="primary" @click="showAllBackers = false">View All</v-btn>
                                        </v-card-actions>
                                    </template>
                                </template>
                            </v-card>
                        </template>
                   </template>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    data(){
        return{
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            isLoading: false,
            backers: [],
            api: "http://localhost:8000/api/",
            showAllBackers: false,
        }
    },
    computed: {
        campaign(){
            return this.$store.getters.getCampaign;
        }
    },
    methods: {
        getBackers(){
            this.isLoading = true
            this.$axios.get(this.api + `campaign_backers/${this.id}/`).then((res) => {
                console.log(res.data)
                this.isLoading = false
                this.backers = res.data
            }).catch(() => {
                this.isLoading = false
            })
        },
    },
    created(){
        this.getBackers()
    }
}
</script>