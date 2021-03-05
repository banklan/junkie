import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import axios from 'axios'
import Routes from './router'
import VeeValidate from 'vee-validate'
import vuetify from './plugins/vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import './styles/style.css'
import './filters'
import {
  store
} from './store';
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import VueGoodShare from 'vue-goodshare'
import Flutterwave from 'flutterwave-vue-v3'

Vue.use(VueRouter)
Vue.use(VeeValidate)
Vue.use(VueGoodShare)
Vue.use(Flutterwave, {
  publicKey: ''
})

Vue.prototype.$axios = axios;

Vue.config.productionTip = false
Vue.component('profile-campaigns', require('./components/child/ProfileCampaigns.vue').default);
Vue.component('my-donations', require('./components/child/MyDonations.vue').default);
Vue.component('what-we-do', require('./components/child/WhatWeDo.vue').default);
Vue.component('popular-campaigns', require('./components/child/PopularCampaigns.vue').default);
Vue.component('fresh-campaigns', require('./components/child/FreshCampaigns.vue').default);
Vue.component('featured-campaigns', require('./components/child/FeaturedCampaigns.vue').default);
Vue.component('success-stories', require('./components/child/SuccessStories.vue').default);
Vue.component('why-choose', require('./components/child/WhyChoose.vue').default);
Vue.component('top-categs', require('./components/child/TopCategs.vue').default);
Vue.component('my-update', require('./components/child/MyCampaignUpdate.vue').default);
Vue.component('add-update', require('./components/child/AddUpdate.vue').default);
Vue.component('my-success-story', require('./components/child/MySuccessStory.vue').default);
Vue.component('our-partners', require('./components/child/OurPartners.vue').default);
// Vue.component('vue-goodshare', )


const router = new VueRouter({
  routes: Routes,
  mode: 'history'
}) 



new Vue({
  vuetify,
  router,
  store,
  components: {
    VueGoodShare
  },
  render: h => h(App),
  // el: '#app',
  template: '<app/>',
}).$mount('#app')
