import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;
axios.defaults.baseURL = "http://localhost:5000/api";
axios.defaults.headers.common["Cache-Control"] = "no-cache";

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
