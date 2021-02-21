<template>
    <div class="what_we_do">
        <v-container>
            <v-row wrap justify="center">
                <div class="text-h4 column-head font-weight-regular mt-12 mb-5">What we do?</div>
            </v-row>
            <v-row wrap justify="center">
                <v-col cols="12" md="4">
                    <v-card raised elevation="6" ripple min-height="400" light>
                        <v-card-title class="justify-center my-2">
                            <v-icon x-large color="primary">mdi-charity</v-icon>
                        </v-card-title>
                        <v-card-text class='justify-center mx-2 title black--text lighten-7'>
                            We help you as individuals, groups, charity organizations and NGO's meet your aspirational goals by providing the means to raise the funds you need.
                        </v-card-text>
                        <v-card-actions class="justify-center mt-3 mb-5">
                            <v-btn large dark color="primary" width="70%" class="mb-6">Start Fundraising</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
                <v-col cols="12" md="4">
                    <v-card elevation="6" raised ripple light min-height="400">
                        <v-card-title class="justify-center my-2">
                            <v-icon x-large color="primary">mdi-head-cog</v-icon>
                        </v-card-title>
                        <v-card-text class="justify-center title black--text lighten-6 mx-2">
                            We provide the tools that helps you bring your creative ideas into reality. Tell us about your project, upload pictures and we will share them with potential sponsors.
                        </v-card-text>
                        <v-card-actions class="justify-center mb-5 mt-3">
                            <v-btn large dark color="primary" width="70%" class="mb-6">Share Your Project</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
        
    </div>
</template>


<style scoped lang="scss">
    .what_we_do{
        .svg_icon_introd{
            height: 4.25rem;
            fill: #ff1744;
        }
        .v-icon{
            font-size: 100px !important;
        }
    }
</style>