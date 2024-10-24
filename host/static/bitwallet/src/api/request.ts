import config from "@/config";
import axios, { AxiosRequestConfig } from "axios";
import { ElMessage } from "element-plus";

const NETWORK_ERROR_MESSAGETEXT = "网络请求错误，请检查网络连接或稍后再试";
//axios实例对象
const service = axios.create({
  baseURL: config.baseApi,
});

//在请求之前做一些事
service.interceptors.request.use((req) => {
  //可以自定义header
  //jwt-token认证的时候
  return req;
});

//在请求之后做一些事
service.interceptors.response.use((res) => {
  //可以对响应数据做一些处理
  const { code, data, msg } = res.data;
  if (code == 200) {
    return data;
  } else {
    //网络请求错误
    ElMessage.error(msg || NETWORK_ERROR_MESSAGETEXT);
    return Promise.reject(msg || NETWORK_ERROR_MESSAGETEXT);
  }
});

//封装的核心函数
function request(options: AxiosRequestConfig<any>) {
  //{}
  options.method = options.method || "get";
  if (options.method.toLowerCase() == "get") {
    options.params = options.data;
  }
  let isMock = config.mock;
  // if (typeof options.mock !== "undefined") {
  //   isMock = options.mock;
  // }
  //对线上环境处理
  if (config.env == "prod") {
    service.defaults.baseURL = config.baseApi;
  } else {
    service.defaults.baseURL = isMock ? config.mockApi : config.baseApi;
  }
  return service(options);
}
export default request;
