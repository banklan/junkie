<template>
    <div class="footer" color="#08192B" light>
        <v-container>
            <v-row wrap align="center" justify="center">
                <v-col cols="12" md="3" offset="1">
                    <p class="white--text" align="start">Join Us</p>
                    <ul class="ml-n6" align="start">
                        <li align="start"><router-link to="/create_new">Start a Kolabo</router-link></li>
                        <li align="start"><router-link to="/how_it_works">How it works</router-link></li>
                        <li align="start"><router-link to="/about-us">About Us</router-link></li>
                        <li align="start"><router-link to="/register">Join Us</router-link></li>
                    </ul>
                </v-col>
                <v-col cols="12" md="3" offset="1">
                    <p class="white--text" align="start">Explore More</p>
                    <ul align="start" class="ml-n6">
                        <li><router-link to="/campaigns">All Campaigns</router-link></li>
                        <li><router-link to="/popular_campaigns">Popular Campaigns</router-link></li>
                        <li><router-link to="/success_stories">Success Stories</router-link></li>
                        <li><router-link to="/login">Login</router-link></li>
                    </ul>
                </v-col>
                <v-col cols="12" md="3" offset="1">
                    <p class="white--text" align="start">Meet Us</p>
                    <ul align="start" class="ml-n6">
                        <li><router-link to="/contact">Contact Us</router-link></li>
                        <li><router-link to="/terms-conditions">Terms & Conditions</router-link></li>
                        <li><router-link to="/privacy-policy">Privacy Policy</router-link></li>
                        <li><router-link to="/faq">FAQ</router-link></li>
                    </ul>
                </v-col>
            </v-row>
        </v-container>
        <v-row justify="center" class="base" align="center">
            <v-col cols="6" class="text-center">
                <v-btn large v-for="icon in icons" :key="icon.name" class="white--text mx-4" icon :href="`${icon.link}`" target="_blank" link>
                    <v-icon :color="icon.color">{{ icon.name }}</v-icon>
                </v-btn>
            </v-col>
            <v-col cols="6" class="text-center">
                <div class="body-2 pt-2 white--text">&copy; {{ new Date().getFullYear() }} kolabo.com All rights reserved </div>
            </v-col>
        </v-row>
    </div>
</template>

<script>
export default {
    data(){
        return{
            icons: [
                {name: 'mdi-facebook', color:'#1877f2', link:'https://www.facebook.com/kolabocampaigns'},
                {name: 'mdi-twitter', color: '#1da1f2', link: 'https://www.twitter.com/kolabocampaigns'},
                {name: 'mdi-instagram', color: '#c32aa3', link: 'https://www.instagram.com/kolabocampaigns'}
            ],
        }
    }
}
</script>

<style scoped lang="scss">
    .footer{
        background-color: #08192B;
        width: 100vw !important;

        p{
            padding-top: 10px;
        }

        ul{
            margin-top: -10px;
            list-style: none;
            text-align: left;

            li{
                line-height: 1.8;

                a{
                    color: #cfcccc;
                    text-decoration: none;
                    font-size: 15px;
                    transition: all .4s;
                    &:hover{
                        color: #fff;
                    }
                }
            }
        }
        .base{
            background-color: #002E4F;
        }       
    }
</style>