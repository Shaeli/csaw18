// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import router from './router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faBolt, faCog } from '@fortawesome/pro-solid-svg-icons'
import { faBluetoothB } from '@fortawesome/free-brands-svg-icons'
import { faLightbulb, faLightbulbOn, faLightbulbSlash, faWifi, faPlusCircle, faLock, faSpinnerThird } from '@fortawesome/pro-light-svg-icons'
import locale from 'element-ui/lib/locale/lang/en'

Vue.use(ElementUI, { locale })

Vue.config.productionTip = false
Vue.use(ElementUI)

library.add(faBolt, faCog, faLightbulb, faLightbulbOn, faLightbulbSlash, faWifi, faPlusCircle, faBluetoothB, faLock, faSpinnerThird)
Vue.component('font-awesome-icon', FontAwesomeIcon)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
