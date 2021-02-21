<template>
    <div class="story_lists">
        <v-container>
            <v-row wrap justify="center" class="mt-8">
                <v-col cols="12" md="8">
                    <div class="text-h4">Success Stories</div>
                </v-col>
            </v-row>
            <v-row wrap justify="start" class="pt-5 pb-7">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                <template v-else>
                    <template v-if="stories.length > 0">
                        <v-col cols="12" md="4" class="justify-space-around" v-for="story in stories" :key="story.id">
                            <v-card elevation="6" light min-height="350" class="mx-auto mb-4 pb-2" :to="{name: 'SuccessStoryShow', params:{id: story.id, slug: story.project.slug}}">
                                <v-img :src="story.project.author.picture" height="250" transition="scale-transition" aspect-ratio="1" alt="Author Picture"></v-img>
                                <v-card-title class="title justify-center mb-2">{{ story.title | capFirstLetter | truncate(120) }}</v-card-title>
                                <v-card-text class="body-text mt-1" align="start">{{ story.details | capFirstLetter | truncate(150) }}</v-card-text>
                            </v-card>
                        </v-col> 
                    </template>
                    <template v-else>
                        <div class="info">There are no success stories to show yet.</div>
                    </template>
                </template>
            </v-row>
        </v-container>
    </div>
</template>


<script>
export default {
    data() {
        return {
            stories: [],
            isLoading: false,
            api: "http://localhost:8000/api/",
        }
    },
    methods: {
        getStories(){
            this.isLoading = true
            this.$axios.get(this.api + 'success_stories/').then((res) => {
                this.isLoading = false
                this.stories = res.data
            }).catch(() => {

            })
        }
    },
    created() {
        this.getStories()
    },
}
</script>


<style lang="scss" scoped>
    a.v-card{
        text-decoration: none !important;
        transition: all .4s !important;

        &:hover{
            box-shadow: 0 10px 7px -6px rgba(0, 0, 0, 0.2), 0 10px 21px 3px rgba(0, 0, 0, 0.14), 0 10px 18px 7px rgba(0, 0, 0, 0.12) !important; 
            transform: scale(1.02);
        }
    }
</style>