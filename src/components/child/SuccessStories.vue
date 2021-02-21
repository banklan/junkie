<template>
    <div class="success_stories">
       <v-container>
           <v-row wrap justify="center" class="mt-8">
               <div class="text-h4 column-head font-weight-regular mt-8 mb-3">
                    Success Stories
                </div>
           </v-row>
           <v-row wrap justify="center" class="mt-8 mb-5" align="center">
                <v-progress-circular v-if="isLoading" indeterminate color="primary" :width="7" :size="70" justify="center" class="mx-auto"></v-progress-circular>
                <template v-else>
                    <v-col cols="12" md="4" v-for="story in stories.slice(0,3)" :key="story.id">
                        <div class="card_box">
                            <div class="img_wrap">
                                <template v-if="story.project.author">
                                    <img :src="story.project.author.picture">
                                </template>
                            </div>
                            <div class="content pb-5">
                                <div class="title">{{ story.title | truncate(60) }}</div>
                                <p>{{ story.details | truncate(180) }}</p>
                                <v-btn outlined class="white--text mb-4" :to="{name: 'SuccessStoryShow', params:{id: story.id, slug: story.project.slug}}">More</v-btn>
                            </div>
                        </div>
                    </v-col>
                </template>
           </v-row>
           <v-row wrap justify="center">
                <div class="cta_btn px-3 mt-3">
                    <v-btn class="secondary white--text" outlined large :to="{name: 'SuccessStoriesList'}">View All</v-btn>
                </div>
           </v-row>
       </v-container> 
    </div>
</template>


<script>
export default {
    data() {
        return {
            stories: [],
            api: "http://localhost:8000/api/",
            isLoading: false,
        }
    },
    methods: {
        getStories(){
            this.isLoading = true
            this.$axios.get(this.api + 'featured_success_stories/').then((res) => {
                this.isLoading = false
                this.stories = res.data
            })
        }
    },
    created() {
        this.getStories()
    },
}
</script>


<style lang="scss" scoped>
    .card_box{
        border-width: thin;
        border: 1px solid #5f5f5f;
        border-radius: 8px;
        white-space: normal;
        display: block;
        transition-property: box-shadow, opacity;
        overflow-wrap: break-word;
        position: relative;
        height: 27rem;
        width: 95%;
        box-shadow: 0 3px 5px rgba(24, 24, 24, 0.72);
        transition: all .5s cubic-bezier(0.215, 0.610, 0.355, 1);
        background: #fff;
        color: #003B63;
        overflow: hidden;

        .img_wrap{
            position: relative;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            overflow: hidden;
            transition: all .5s cubic-bezier(0.215, 0.610, 0.355, 1);

            img{
                position: absolute;
                opacity: 1;
                top: 0;
                left: 0;
                width: 100%;
                height: 80%;
                display: block;
                transition: 0.5s ease;
            }
        }
        .content{
            position: absolute;
            left: 0;
            bottom: 0;
            height: 90px;
            width: 100%;
            background: #003B63;
            overflow: hidden;
            box-sizing: border-box;
            color: #fff;
            padding-top: 20px;
            font-family: 'Lato', sans-serif;
            transition: all .4s ease;

            .title{
                font-size: 23px !important;
                font-weight: 300 !important;
                line-height: 1.6;
                margin-top: -5px;
                padding: 5px 10px;
            }
            p{
                opacity: 0;
                font-size: 18px;
                line-height: 1.8;
                padding: 12px;
                font-weight: 200 !important;
            }
        }

        &:hover{
            cursor: pointer;
            border: 1px solid rgb(143, 143, 143);
            box-shadow: 0px 2px 20px 13px rgb(111 111 111/72%);

            .img_wrap img{
                opacity: .80;
                transform: scale(1.2) translateY(-2rem);
            }
            .content{
                height: 85%;
                bottom: 0;

                p{
                    opacity: 1;
                }
            }
        }
    }
</style>