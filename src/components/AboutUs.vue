<template>
    <div class="about">
        <div class="banner"></div>
        <v-container>
            <v-row wrap justify="center" align="center">
                <v-col cols="12" md="8">
                    <v-card shaped light flat min-height="100" class="mt-5">
                        <v-card-title class="primary white--text justify-center">
                            About Us
                        </v-card-title>
                        <v-card-text class="body-text-bg mt-5" align="start">
                            <p> Welcome to Kolabo, an online resource dedicated to helping you raise the funds you need to pay for that medical emergency, fund your NGO projects, help bring that creative project to life,
                                help save our planet from environmental destruction, pay for those indigent students tuition fees etc.
                            </p>
                            <p> We are a team of enthusiasts committed to helping you share your inspirations, dreams and stories. 
                                However, at Kolabo, we believe that fundraising should not just be about hitting the donate button and consumating a monetary transaction, rather, it should be about building 
                                relationships that are truely committed to helping you to stay alive; offer you a lifeline to survive those harrowing dark moments of life; helping you grow; helping you bring
                                 those beautiful dreams into reality and ultimately, inspires well wishes, prayers, actions and deep commitments to each other's cause. 
                            </p>
                            <p>Our mission is to help build a closely-knit family-like bonds between beneficiaries of campaigns and the backers.</p>
                            <p>
                                We are a brand borne out of a pressing desire to provide a customized tool that incredibly simplifies fundraising for any cause and purpose. With our sharing tools, 
                                we help you harness the powerful magic of social media to propagate your stories and take your dreams to the world. 
                                Your campaigns are guaranteed to be seen by thousands of daily visitors to our sites and millions more on the social media feeds.
                            </p>
                            <p>
                                A significant part of our processes is carrying out a bit of due diligence on every campaign before publishing them. This is to ensure that fraudsters and bots do not take undue advantage of our platform to publish fake stories & non-existing creatives.
                                While we cannot absolutely guarantee the detection of all fake profiles and fraudulent campaigns, we will continue to strive by putting processes in place to ensure that every campaign published are borne out of genuine concerns. 
                                And for any fraudulent campaign detected, we will not hesitate in deleting the profiles and the campaigns. 
                            </p>
                            <p>
                                What's more? We make use of the safest payment processors, which guarantees you peace of mind when you use your cards on our platform. 
                            </p>
                            <p> At Kolabo, we are inspired by the belief of the responsibilty to each other, the generation yet unborn and to our planet, to help each other stay alive and healthy, become better, achieve our individual and collective goals, to make our communites and the world safer, 
                                help indigent kids and orphans get quality education and lead quality lives, 
                                help bring creators dreams to reality and ultimately, help make the world a better place.</p>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<style lang="scss" scoped>
    .about{
        .banner{
            height: 16rem;
            width: 100%;
            background-image: url('../assets/images/about.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .about_text{
            line-height: 1.7;
        }
    }
</style>