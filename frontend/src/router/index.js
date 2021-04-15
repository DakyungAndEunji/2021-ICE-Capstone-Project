import Vue from "vue";
import VueRouter from "vue-router";
import Temperature from "../views/Temperature.vue";
import ProductList from "../views/ProductList.vue";

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
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
