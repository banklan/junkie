import Vue from 'vue'
import Vuetify from 'vuetify'
// import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify)

const opts = {
    theme:{
         themes: {
            light: {
                primary: '#003B63',
                // primary: '#3a86ff',
                // primary: '#ff1744',
                pry_light: '#0063ab',
                // secondary: '#002E4F',
                secondary: '#ff1744',
                error: '#b71c1c',
                lightbg: '#fff',
            },
        },
    }
}

export default new Vuetify(opts)
