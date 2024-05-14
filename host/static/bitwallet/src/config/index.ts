/**
 *
 * 环境配置文件
 * 1.开发
 * 2.测试
 * 3.线上
 *
 *
 */

const env =  "development";

const EnvConfig = {
  development: {
    baseApi: "/api",
    mockApi: "https://www.fastmock.site/mock/api",
  },
  test: {
    baseApi: "/api",
    mockApi: "https://www.fata",
  },
  production: {
    baseApi: "//future.com/api",
    mockApi: "https://www.fata",
  },
};
export default {
  env,
  mock: true,
  ...EnvConfig[env],
};
