<template>
    <div class="why_choose">
       <v-container>
           <v-row wrap justify="center" class="mt-8">
               <div class="text-h4 column-head font-weight-regular mt-8 mb-3">
                    Why Choose Kolabo?
                </div>
           </v-row>
           <v-row wrap justify="center" class="mt-8 mx-4" align="center">
                <v-col cols="12" md="4">
                    <div class="card">
                        <div class="icon_wrap">
                            <v-icon x-large color="white">mdi-radio-tower</v-icon>
                            <div class="title mb-3">Wide Reach</div>
                        </div>
                        <div class="details text-center">
                            <p>Your campaign is guaranteed to be seen by a huge audience as of thousands of daily visitors to our app. </p>
                        </div>
                    </div>  
                </v-col>
                <v-col cols="12" md="4">
                    <div class="card">
                        <div class="icon_wrap">
                            <v-icon x-large color="white">mdi-rocket-launch</v-icon>
                            <div class="title mb-3">Fast Payout</div>
                        </div>
                        <div class="details text-center">
                            <p>When your campaign expires & you complete your payment request page, we will transfer the proceeds of your campaign to your account swiftly.</p>
                        </div>
                    </div>  
                </v-col>
                <v-col cols="12" md="4">
                    <div class="card">
                        <div class="icon_wrap">
                            <v-icon x-large color="white">mdi-shield-lock-outline</v-icon>
                            <div class="title mb-3">Secure</div>
                        </div>
                        <div class="details text-center">
                            <p>We partner with some of the most secure & reliable payment processing platforms around, so your transactions are safe. </p>
                        </div>
                    </div>  
                </v-col>
           </v-row>
       </v-container> 
    </div>
</template>


<style lang="scss" scoped>
    .card{
        border-width: thick;
        border:1px solid #929292;
        border-radius: 8px;
        white-space: normal;
        display: block;
        transition-property: box-shadow, opacity;
        overflow-wrap: break-word;
        position: relative;
        height: 25rem;
        width: 100%;
        box-shadow: 0 3px 5px rgba(24, 24, 24, 0.72);
        transition: all .6s cubic-bezier(0.215, 0.610, 0.355, 1);
        background: #003B63;
        color: #fff;
        overflow: hidden;

        .icon_wrap{
            position: relative;
            top: 40%;
            height: 100%;
            width: 100%;
            transition: all .4s ease-in-out;

            .v-icon{
                position: absolute;
                font-size: 10rem !important;
                transform: translate(-50%, -50%);
                // transition: all .6s ease-in-out;
            }
            .title{
                position: absolute;
                bottom: 50%;
                left: 50%;
                font-size: 30px !important;
                font-weight: 300 !important;
                transform: translate(-50%, -50%);
            }
        }
        .details{
            position: relative;
            bottom: 0;
            opacity: 0;
            color: #3a3a3a;
            transition: all .6s cubic-bezier(0.215, 0.610, 0.355, 1);
            margin-top: 25px !important;
            
            p{
                font-size: 18px !important;
                font-family: 'Lato', sans-serif;
                padding: 15px;
                line-height: 1.8;
            }
        }

        &:hover{
            cursor: pointer;
            border: 1px solid rgb(218, 218, 218);
            box-shadow: 0px 2px 20px 13px rgb(111 111 111/72%);
            background: #fff;

            .icon_wrap{
                transform: translateY(-20%);

                .v-icon{
                    font-size: 6rem !important;
                    color: #0043ff !important;
                }
                .title{
                    color: #0043ff;
                    font-weight: 400 !important;
                    top: 30%;
                    transform: translate(-50%, -70%);
                }
            }
            .details{
                opacity: 1;
                bottom: 20%;
                transform: translateY(-100%);
                margin-top: 25px !important;
            }
        }
    }
</style>