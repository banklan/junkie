<template>
    <div class="faq">
        <div class="banner"></div>
        <v-container>
            <v-row wrap justify="center" align="center">
                <v-col cols="12" md="8">
                    <v-card shaped light flat min-height="100" class="mt-5">
                        <v-card-title class="primary white--text mb-3 justify-center">
                            Frequently Asked Questions
                        </v-card-title>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">How do i start a Kolabo fundraising campaign?</p>
                            <p class="">To start a kolabo campaign, be sure your cause is genuine. <router-link to="/register">Register </router-link> or <router-link to="/login">login </router-link> to create a campaign.</p>
                            <p>Go to the <router-link to="/create-new">create new link</router-link>, set a title, write your story, set the xpiry date and the goal, upload pictures and post.</p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">Who can start a campaign?</p>
                            <p>Anyone above the age of 18 can start a kolabo campaign.</p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">Can i set up a Kolabo campaign for another person/group?</p>
                            <p>Yes you can. Kindly ensure that you state the name of the beneficiary while setting up the campaign.</p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">What can i raise funds for?</p>
                            <p>You can start a kolabo campaign to raise fund for just about anything. To raise funds for a medical emergency; To raise funds to finance the production of that innovation you are working on;
                                To finance a research; To pay tuition fees of students; To organise a youth sport tournament; To fund your NGO projects..etc. </p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">How long can a campaign run?</p>
                            <p>You can set up your campaign to run for as long you want. You can also extend the expiry of a campaign once, to enable you more time to raise funds. </p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">What happens if i dont reach my goal?</p>
                            <p>We do not require that you meet your goal. Whenever your campaign expires and you request withdrawal, your fund will be transferred to your bank account after our charges have been deducted. </p>
                            <p>However, we do encourage campaigners to try share their campaigns on their social medias and send via mails and sms to their families, friends and loved ones so they can achieve their goals.</p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">What do i need to set up a kolabo fundraising campaign?</p>
                            <p>To register on kolabo, you only need to have a functional email address, which serves as your username.</p>
                            <p>However, to set up a kolabo campaign, <span class="font-weight-bold">you will need to update your profile page to include your valid means of identification (ID card), your active mobile phone number,
                                and your address. You will also need to supply your bank account details </span> to enable us process your withdrawals when due.
                            </p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">How do i get donations for my campaigns?</p>
                            <p>Our app receives thousands of visitors daily. If you set up your campaign properly with clear objectives and easy-to-relate with stories, backers are more likely to sympathise with/believe in your cause and donate.</p>
                            <p>We have also integrated effective social media sharing means so that you can share your campaigns on any major social media, email and sms to your families, friends and loved ones. </p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">If i set up a kolabo campaign on behalf of a beneficiary, can the benefiacy access/request for withdrawal of the fund? </p>
                            <p>No. Since your kolabo account is personalized and you are not expected to share the credentials to the account with anyone, you should be the one to have access to withdraw the fund. </p>
                            <p>However, you can change the account details attached to your profile to that of the benefiary, so at withdrawal, he/she gets the fund.</p>
                            <p>Do not hesitate to <router-link to="/contact">contact us</router-link> if you need to change the account details attached to your profile.</p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">How much does it cost to set up a kolabo campaign?</p>
                            <p>It is absolutely free to set up a kolabo campaign.</p>
                            <p>However, we charge you a fee which comprises the inevitable bank charges, VAT and a token for the upkeep of the app. It amount to 11% of the total amount raised. The charges are deducted before withdrawal. </p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">What is the maximum amount i can raise on kolabo?</p>
                            <p>We do not place a limit on what you can raise on kolabo. You can set your campaign goals depending on what your needs are. </p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">How safe is my donation?</p>
                            <p>Your donation is safe with kolabo. We have integrated one of the safest payment processors available.</p>
                        </v-card-text>
                        <v-card-text class="body-text" align="start">
                            <p class="font-weight-bold primary--text">How soon can i get my fund after requesting withdrawal?</p>
                            <p>Once your details are verified, you will get your fund within 24 hours of request.</p>
                        </v-card-text>
                        <v-card-actions class="justify-center pb-8 mb-8">
                            <v-btn dark color="secondary" x-large to="/create_new">Start A Kolabo</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<style lang="scss" scoped>
    .faq{
        font-family: 'Roboto', sans-serif !important;
        .banner{
            height: 16rem;
            width: 100%;
            background-image: url('../assets/images/how.jpg');
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
    }
</style>