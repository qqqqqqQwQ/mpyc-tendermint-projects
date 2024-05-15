import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ElementPlus from "element-plus";
import axios from "axios";
import VueAxios from "vue-axios";
import "element-plus/dist/index.css";
import './api/mock.ts'; 
import api from "./api/api";
const app = createApp(App);
app.use(ElementPlus);
app.use(store);
app.use(VueAxios, axios);
app.use(router);
app.config.globalProperties.$api=api
// 使用 provide 方法提供 Axios 实例
app.provide("$axios", axios);

app.mount("#app");
 