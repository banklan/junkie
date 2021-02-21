<template>
    <div class="success_story">
        <v-container>
            <v-row wrap justify="start" class="mt-8">
                <v-col cols="3" md="2">
                    <v-btn rounded color="secondary" dark elevation="3" left @click.prevent="$router.go(-1)"><v-icon left>arrow_left</v-icon> Back</v-btn>
                </v-col>
                <v-col cols="9" md="10">
                    <div class="title">Success Story</div>
                </v-col>
            </v-row>
            <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
            <v-row wrap justify="center" class="mt-2" v-else>
                <v-col cols="12" md="8">
                    <v-card light flat elevation="6" min-height="250" class="mt-5 py-3 px-3">
                        <v-card-title class="justify-center title">{{ story.title | capFirstLetter }} </v-card-title>
                        <v-card-text align="start" class="body-text"> {{ story.details | capFirstLetter }}</v-card-text>
                        <v-card-text align="start" class="font-italic display">{{ story.date }}</v-card-text>
                    </v-card>
                </v-col>
                <v-col cols="12" md="4">
                    <v-card light flat elevation="6" min-height="300" class="mt-5">
                        <v-card-title class="primary white--text justify-center">Details</v-card-title>
                        <v-card-text align="start" class="mt-3">
                            <table class="table table-hover table-striped">
                                <tbody>
                                    <tr>
                                        <th scope="row">Campaign</th>
                                        <td><router-link :to="{name: 'CampaignShow', params: {id: story.project.id, slug: story.project.slug}}">{{ story.project.title }}</router-link></td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Campaigner</th>
                                        <td>{{ story.project.author.fullname }}</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Beneficiary</th>
                                        <td>{{ story.project.beneficiary ? story.project.beneficiary : 'Self' }}</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Published</th>
                                        <td>{{ story.project.created}}</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Expiry</th>
                                        <td>{{ story.project.expiry}}</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Goal</th>
                                        <td>&#8358;{{ story.project.goal | price }}</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Total Donations</th>
                                        <td>&#8358;{{ story.project.total_donations | price }}</td>
                                    </tr>
                                    <tr>
                                        <th scope="row">Percent Raised</th>
                                        <td>{{ story.project.percent_raised }}%</td>
                                    </tr>
                                </tbody>
                            </table>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>


<script>
export default {
    data() {
        return {
            id: this.$route.params.id,
            slug: this.$route.params.slug,
            story: null,
            api: "http://localhost:8000/api/",
            isLoading: false,
        }
    },
    methods: {
        getStory(){
            this.isLoading = true
            this.$axios.get(this.api + `success_stories/${this.id}/`)
            .then((res) => {
                this.isLoading = false
                this.story = res.data
            })
        }
    },
    created() {
        this.getStory()
    },
}
</script>


<style scoped lang="scss">
    .v-card{
        .v-card__text{
            a{
                text-decoration: none !important;
            }
        }
    }
</style>