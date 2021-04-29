import Vue from "vue";
import VueRouter from "vue-router";
import Temperature from "../views/Temperature.vue";
import ProductList from "../views/ProductList.vue";
import Statistics from "../views/Statistics.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Temperature",
    component: Temperature,
  },
  {
    path: "/productList",
    name: "ProductList",
    component: ProductList,
  },
  {
    path: "/Statistics",
    name: "Statistics",
    component: Statistics,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
