import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex, axios);


const proj = window.localStorage.getItem('campaign')
const campaign = proj ? JSON.parse(proj) : null

const is_auth = window.localStorage.getItem('auth-token')
const auth_token = is_auth ? is_auth : null

const is_login = localStorage.getItem('auth-user')
const authUser = is_login ? JSON.parse(is_login) : null

const campaign_to = localStorage.getItem('campaign_to_back')
const campaignToBack = campaign_to ? JSON.parse(campaign_to) : null

const don = localStorage.getItem('backing')
const donation_data = don ? JSON.parse(don) : null

const create = localStorage.getItem('new_campaign')
const new_campaign = create ? JSON.parse(create) : null

const mod_camp = localStorage.getItem('mod_campaign')
const modCampaign = mod_camp ? JSON.parse(mod_camp) : null

const trx_ref = localStorage.getItem('trx-ref')
const ref = trx_ref ? trx_ref : null

export const store = new Vuex.Store({
    state: {
        campaign: campaign,
        auth_token: auth_token,
        authUser: authUser,
        campaign_to_back: campaignToBack,
        donation_data: donation_data,
        new_campaign: new_campaign,
        mod_campaign: modCampaign,
        redirect_route: null,
        ref: ref
    },
    getters: {
        getCampaign(state){
            return state.campaign;
        },
        getToken(state){
            return state.auth_token;
        },
        getAuthUser(state){
            let authUser = state.auth_token ? state.authUser : null 
            return authUser
        },
        isLoggedIn(state){
            if(state.auth_token !== null){
                return true
            }else{
                return false
            }
        },
        campaignIsMine(state)
        {
            if (state.auth_token) {
                let author = state.authUser.id
                let campaign = state.campaign.author.id
                if (author === campaign) {
                    return true
                } else {
                    return false
                }
            }
        },
        campaignToBack(state)
        {
            return state.campaign_to_back
        },
        backing(state)
        {
            return state.donation_data
        },
        newCampaign(state)
        {
            return state.new_campaign
        },
        getFollowers(state)
        {
            let followers = state.campaign.followers.length
            return followers
        },
        getCampaignToModify(state)
        {
            return state.mod_campaign
        },
        getRedirectRoute(state)
        {
            return state.redirect_route
        },
        getTrxref(state)
        {
            return state.ref
        }
    },
    actions: {
        getAuthUser(context){
            let token = window.localStorage.getItem('auth-token')
            const config = {
                headers: {
                    'Authorization': 'Token '+ token
                }
            }
            axios.get('http://localhost:8000/api/profile/', config).then((res) => {
                context.commit('set_user', res.data)
                localStorage.setItem('auth-user', JSON.stringify(res.data))
                console.log(res.data)
            })
        },
    },
    mutations: {
        store_campaign(state, payload){
            state.campaign = payload
            localStorage.setItem('campaign', JSON.stringify(payload))
        },
        store_token(state, payload)
        {
            state.auth_token = payload
            localStorage.setItem("auth-token", payload);
        },
        set_user(state, payload){
            state.authUser = payload
        },
        logout(state){
            window.localStorage.removeItem('auth-token')
            window.localStorage.removeItem('auth-user')
            window.localStorage.removeItem('backing')
            window.localStorage.removeItem('campaign_to_back')
            state.auth_token = null
            state.authUser = null
        },
        campaign_to_back(state, payload)
        {
            state.campaign_to_back = payload
            localStorage.setItem('campaign_to_back', JSON.stringify(payload))
        },
        donation_data(state, payload)
        {
            state.donation_data = payload
            localStorage.setItem('backing', JSON.stringify(payload))
        },
        store_new(state, payload)
        {
            localStorage.setItem('new_campaign', JSON.stringify(payload))
        },
        store_new2(state, payload)
        {
            // console.log(payload)
            let first = localStorage.getItem('new_campaign')
            if(first){
                let parsed = JSON.parse(first)
                parsed.title = payload.title
                parsed.goal = payload.goal
                parsed.details = payload.details
                localStorage.setItem('new_campaign', JSON.stringify(parsed))
            }
        },
        redirect_onlogin(state, payload)
        {
            state.redirect_route = payload
        },
        clear_redirect(state)
        {
            state.redirect_route = null
        },
        genTrxRef(state)
        {
            var ref = ""
            var chars = "abcdefghijklmnopqrstuvwxyz0123456789"
            for (var i=0; i<12; i++){
                ref += chars.charAt(Math.floor(Math.random() * chars.length))
            }
            localStorage.setItem('trx-ref', ref)
            state.trxRef = ref 
        }
    }
})
