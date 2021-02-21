<template>
  <nav>
    <v-app-bar flat light color="lightbg">
      <span class="hidden-md-and-up">
        <v-app-bar-nav-icon class="secondary--text hidden-md-and-up" @click="sidebar = true"></v-app-bar-nav-icon>
      </span>
      <v-toolbar-title class="ml-5 my-2">
        <router-link to="/" tag="span" style="cursor:pointer" exact>
            <img src="../../media/images/kolabo-logo2.png" height="60">
        </router-link>
      </v-toolbar-title>
      
      <v-spacer></v-spacer>
      <!-- {{ isMine }} -->
      <span class="search">
        <input type="text" placeholder="Search Campaigns..." v-model="q" @keyup.enter="searchCampaign">
        <v-icon>search</v-icon>
      </span>
      <span v-if="authUser" class="mr-3">Welcome {{ authUser.first_name | capFirstLetter }}</span>
      <v-toolbar-items class="hidden-sm-and-down menu_items">
        <router-link v-for="item in menuItems" :key="item.title" :to="item.path">{{ item.title }}</router-link>
        <template v-if="isLoggedIn">
          <router-link v-for="item in authMenuItems" :key="item.title" :to="item.path">{{ item.title }}</router-link>
          <button type="button" class="" @click="logout">Logout</button>
        </template>
        <template v-else>
          <router-link v-for="item in nonAuthMenuItems" :key="item.title" :to="item.path">{{ item.title }}</router-link>
        </template>
     </v-toolbar-items>
    </v-app-bar>
    <v-navigation-drawer absolute v-model="sidebar" class="hidden-md-and-up" disable-resize-watcher>
      <v-toolbar-title align="center" class="my-3">
          <router-link to="/" tag="span" style="cursor:pointer" exact>
              <img src="../../media/images/kolabo-logo1.png" height="100">
          </router-link>
      </v-toolbar-title>
      <v-divider></v-divider>
      <v-list light class="ml-4" align="start">
          <v-list-item class="primary--text" v-for="item in menuItems" :key="item.title" link :to="item.path">
              <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
          </v-list-item>
          <template v-if="isLoggedIn">
              <v-list-item class="primary--text" v-for="item in authMenuItems" :key="item.title" link :to="item.path">
                  <v-list-item-content>
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
              </v-list-item>
          </template>
          <template v-else>
              <v-list-item class="primary--text" v-for="item in nonAuthMenuItems" :key="item.title" link :to="item.path">
                  <v-list-item-content>
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
              </v-list-item>
          </template>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      sidebar: false,
      menuItems: [
        { title: "All Campaigns", path: "/campaigns", icon: "mdi-group" },
        { title: "About", path: "/about-us", icon: "mdi-view-dashboard" },
        { title: "Contact", path: "/contact", icon: "mdi-group" },
        { title: "Create", path: "/create_new", icon: "mdi-group" },
      ],
      authMenuItems: [
        { title: "Profile", path: "/profile", icon: "folder" },
      ],
      nonAuthMenuItems: [
        { title: "Login", path: "/login", icon: "folder" },
        { title: "Register", path: "/register", icon: "user" }
      ],
      loggedOut: false,
      q: '',
      api: "http://localhost:8000/api/",
      isSearching: false
    }
  },
  computed: {
      authToken() {
        return this.$store.getters.getToken;
      },
      authUser() {
        return this.$store.getters.getAuthUser;
      },
      isLoggedIn(){
        return this.$store.getters.isLoggedIn
      },
      isMine(){
        return this.$store.getters.campaignIsMine
      }
  },
  methods: {
      logout() {
          if (this.authToken) {
            this.$store.commit("logout");
            if (this.$route.path != "/") {
              this.$router.push("/");
            }
            this.loggedOut = true;
          }
      },
      searchCampaign(){
          if(this.q.trim() !== ''){
              // this.isSearching = true
              let q = this.q.trim()
              this.$router.push({name: 'CampaignSearchResults', query:{q: q}})
          }
      }
  },
};
</script>

<style lang="scss" scoped>
  nav{
    width: 100vw !important;
  }
  .v-app-bar {
    height: 70px !important;
    background-color: transparent !important;
    width: 100vw !important;
    margin: 0;
    margin-top: 7px !important;
    color: #333 !important;

    .search{
      padding-right: 30px;
      position: relative;
      width: 20rem !important;

      input{
        width: 34%;
        border: 1px solid #d3d2d2;
        border-radius: 100px;
        outline: none !important;
        padding: .25rem 1rem;
        font-family: inherit;
        font-size: inherit;
        background-color: #f7f7f7;
        transition: .3s ease;

        &:focus{
          outline: none;
          width: 100%;
          background-color: #fcfcfc;
        }
        &::-webkit-input-placeholder{
          font-weight: 100;
          color: #b9b9b9;
        } 
      }
      input:focus + .v-icon{
        color: #b9b9b9
      }
      .v-icon{
        color:#b9b9b9;
        margin-left: -30px;

        &:focus{
          outline: none;
        }
      }

    }
    // margin-bottom: auto;
  }
  .v-toolbar__title {
    font-family: "Baloo 2", cursive;
    font-weight: 600;
    font-size: 28px !important;
    color: #003B63 !important;
    .ji{
      color: #ff1744 !important;
    }
  }
  .v-toolbar__items a.v-btn--active {
    background: none !important;
  }

  .menu_items {
    width: 40%;
    display: flex;
    justify-content: space-around;
    align-items: center;

    button {
      text-transform: capitalize;
      font-size: inherit;
      padding-left: 15px !important;
      transition: all 0.6s !important;
      padding: 6px 12px !important;
      border-radius: 50px;

      &:hover {
        background: #003b63;
        color: #fff !important;
        text-transform: none;
        border-radius: 100px;
      }
    }

    a {
      padding-right: 10px;
      text-decoration: none;
      transition: all 0.4s;
      padding: 6px 12px;
      color: rgb(61, 61, 61) !important;
      font-weight: 400 !important;

      &:focus {
        outline: none;
      }
      &:hover,
      &.router-link-active,
      &.router-link-exact-active {
        background: #003b63;
        color: #fff !important;
        text-transform: none;
        border-radius: 100px;
      }
    }
  }
  .v-navigation-drawer{
  .v-divider{
    border-color: #144A6F !important;
  }
   button{
    text-transform: capitalize;
    font-size: inherit;
    transition: all 0.6s !important;
    margin-left: -10px;
    padding: 10px !important;
    border-radius: 100px;
    color:  rgb(61, 61, 61) !important;

    &:hover {
      background: #144A6F;
      color: #fff !important;
      text-transform: none;
      border-radius: 100px;
      padding: 10px 25px 10px 10px !important;
    }
   }
}
</style>
