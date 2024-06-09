import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import LoginView from "../views/LoginView.vue";

import MainView from "../views/MainView.vue";
const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "home",
    component: () => import("@/views/HomeView.vue"),
  },
  {
    path: "/loginhome",
    name: "loginhome",
    component: () => import("@/views/LoginHome.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterView.vue"),
  },
  {
    path: "/main",
    name: "main",
    component: import("@/views/NavigateView.vue"),
  },
  {
    path: "/testone",
    name: "TestOne",
    component: () => import("@/views/TestOneView.vue"),
  },
  {
    path: "/testtwo",
    name: "TestTwo",
    component: () => import("@/views/TestTwoView.vue"),
  },
  {
    path: "/personinfo",
    name: "personinfo",
    component: () => import("@/views/PersonInfoView.vue"),
  },
  {
    path: "/setting",
    name: "setting",
    component: () => import("@/views/SettingView.vue"),
  },
  {
    path: "/aboutus",
    name: "aboutus",
    component: () => import("@/views/AboutUs.vue"),
  },
  {
    path: "/evaluation",
    name: "evaluation",
    component: () => import("@/views/EvaluationView.vue"),
  },
  {
    path: "/borrowinformation",
    name: "borrowinformation",
    component: () => import("@/views/BorrowInformationView.vue"),
  },
  {
    path: "/borrowmain",
    name: "borrowmain",
    component: () => import("@/views/BorrowMainView.vue"),
  },
  {
    path: "/modelfunction",
    name: "modelfunction",
    component: () => import("@/views/ModelFunctionView.vue"),
  },
  {
    path: "/selectmodel",
    name: "selectmodel",
    component: () => import("@/views/SelectModelView.vue"),
  },
  {
    path: "/submitdeposit",
    name: "submitdeposit",
    component: () => import("@/views/SubmitDepositView.vue"),
  },
  // {
  //   path: '/register',
  //   name: 'register',
  //   component: RegisterView
  // },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
