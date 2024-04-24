import axios, { AxiosRequestConfig, AxiosResponse } from "axios";
import { ElLoading } from "element-plus";
import { ElMessage } from "element-plus";

let loading: any;
const http = axios.create({
  baseURL: "/api",
  timeout: 5000,
});
const startLoading = () => {
  interface Options {
    lock: boolean;
    text: string;
    background: string;
  }
  const options: Options = {
    lock: true,
    text: "Loading",
    background: "rgba(0, 0, 0, 0.7)",
  };
  loading = ElLoading.service(options);
};
const endLoading = () => {
  loading.close();
};

// 添加请求拦截器
http.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    startLoading();
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });
// // 请求拦截
// http.interceptors.request.use((config: AxiosRequestConfig<any>) => {
//   // 开始Loading
//   startLoading();
//   return config;
// });

// 响应拦截
http.interceptors.response.use(
  (res: AxiosResponse<any, any>) => {
    // 结束Loading
    endLoading();
    // console.log('成功响应拦截',res)
    // 如果请求成功直接返回响应数据
    if (res.status === 200) {
      return res.data;
    }
  },
  (error) => {
    // 结束Loading
    endLoading();
    // console.log('失败响应拦截',error)
    const { response: res } = error;
    const msg =
      typeof res.data === "string"
        ? res.data
        : res.data.error || "请求失败，请稍后重试";
    ElMessage.error(msg);
    // 错误提醒
    return Promise.reject(error);
  }
);

export default http;
