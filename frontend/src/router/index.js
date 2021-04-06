import Vue from "vue";
import VueRouter from "vue-router";
import Temperature from "../views/Temperature.vue";
import Product from "../views/Product.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Temperature",
    component: Temperature,
  },
  {
    path: "/product",
    name: "Product",
    component: Product,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
