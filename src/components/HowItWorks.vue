<template>
    <div class="how_it_works">
        <div class="banner"></div>
        <v-container>
            <v-row wrap justify="center" class="mt-8">
                <div class="headline">How It Works</div>
            </v-row>
            <v-row wrap justify="center" align="center">
                <v-col cols="12" md="8">
                    <v-card shaped light flat min-height="100" class="mt-5">
                        <v-card-title class="primary white--text mb-3">
                            Start Your Kolabo
                        </v-card-title>
                        <v-card-text class="body-text" align="start">
                            <table class="table table-borderless table-responsive">
                                <tr>
                                    <th>1</th>
                                    <td>To start a Kolabo, <router-link to="/login">log in</router-link> or <router-link to="/register">register</router-link> if you are not a member.</td>
                                </tr>
                                <tr>
                                    <th>2</th>
                                    <td>Click on <router-link to="/create_new">the create new link</router-link>, write an appropriate title and tell your story.</td>
                                </tr>
                                <tr>
                                    <th>3</th>
                                    <td>Fill every detail required in the forms, including category, beneficiary name, the target amount (goal) and the campaign expiry among other things.</td>
                                </tr>
                                <tr>
                                    <th>4</th>
                                    <td>Upload a picture for your campaign. To upload more pictures, kindly update your campaign.</td>
                                </tr>
                                <tr>
                                    <th>5</th>
                                    <td>Submit your campaign and await our approval. Campaigns do not show on our site until approved.</td>
                                </tr>
                            </table>
                        </v-card-text>
                        <v-card-actions class="justify-center pb-8 mb-8">
                            <v-btn dark color="secondary" x-large to="/create_new">Start A Kolabo</v-btn>
                        </v-card-actions>
                    </v-card>
                    <v-card shaped light flat min-height="100" class="mt-2">
                        <v-card-title class="primary white--text mb-3">
                            Share Your Kolabo With Family & Friends
                        </v-card-title>
                        <v-card-text class="body-text" align="start">
                            <table class="table table-borderless table-responsive">
                                <tr>
                                    <td>Share your campaign(s) on social media, via mails, text messages etc to your family & friends.</td>
                                </tr>
                            </table>
                        </v-card-text>
                    </v-card>
                    <v-card shaped light flat min-height="100" class="mt-2">
                        <v-card-title class="primary white--text mb-3">
                            Manage Donations & Feedbacks
                        </v-card-title>
                        <v-card-text class="body-text" align="start">
                            <table class="table table-borderless table-responsive">
                                <tr>
                                    <th>1</th>
                                    <td>Track your donations on your profile page.</td>
                                </tr>
                                <tr>
                                    <th>2</th>
                                    <td>Give an update on the campaign when necessary.</td>
                                </tr>
                                <tr>
                                    <th>3</th>
                                    <td>At the expiry of your campaign, accept and withdraw your funds.</td>
                                </tr>
                                <tr>
                                    <th>4</th>
                                    <td>Use updates to appreciate and say thank you to backers.</td>
                                </tr>
                                <tr>
                                    <th>5</th>
                                    <td>After withdrawal, write a success story telling backers and followers about how helpful the donations were.</td>
                                </tr>
                            </table>
                        </v-card-text>
                    </v-card>
                    <v-card shaped light flat min-height="100" class="mt-2">
                        <v-card-title class="primary white--text mb-3">
                            To back a kolabo campaign
                        </v-card-title>
                        <v-card-text class="body-text" align="start">
                            <table class="table table-borderless table-responsive">
                                <tr>
                                    <th>1</th>
                                    <td>Open the campaign to back.</td>
                                </tr>
                                <tr>
                                    <th>2</th>
                                    <td>Click on the <span class="font-weight-bold">Back Campaign</span> button (You must be logged in to donate/back a campaign).</td>
                                </tr>
                                <tr>
                                    <th>3</th>
                                    <td>You will get redirected to our payment gateway. Fill the checkout forms on the page and leave a message for the campaigner.</td>
                                </tr>
                                <tr>
                                    <th>4</th>
                                    <td>Submit and your donations will be received.</td>
                                </tr>
                            </table>
                        </v-card-text>
                        <v-card-actions class="justify-center pb-8 mb-8">
                            <v-btn dark color="secondary" x-large to="/campaigns">Back A Campaign</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<style lang="scss" scoped>
    .how_it_works{
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