import { createStore } from 'vuex';

export default createStore({
  state: {
    dataContainer: ['数据1', '数据2', '数据3'], //存放数据的地方,可修改
    modelContainer: ['模型1', '模型2', '模型3'], //存放模型的地方,可修改
    userData: {
      username: '',//默认用户名
      deposit: 0,//押金金额,默认为0,可修改
      fund: 0,//资金金额,默认为0,可修改
    },
    userRequests: [
      {
        id: 0,
        data: '',
        model: '',
        state: '',
      },
    ],
    depositModified:-100,//每个请求完成时扣除的押金金额即服务费,可修改
    fundModified:200,//每个请求完成时分配的资金,可修改
  },
  getters: {},
  mutations: {
    resetUser(state) {
      state.userData.username = '';
      state.userData.deposit = 0;
      state.userData.fund = 0;
      //登出时重置用户的参数,默认下一个登录的用户初始押金和资金为0,可修改
    },
    updateUsername(state, amount: string) {
      state.userData.username = amount;
    },
    updateDeposit(state, amount: number) {
      state.userData.deposit += amount;
    },
    updateFund(state, amount: number) {
      state.userData.fund += amount;
    },
    updateData(state, amount: string) {
      state.userRequests[state.userRequests.length - 1].data = amount;
    },
    updateModel(state, amount: string) {
      state.userRequests[state.userRequests.length - 1].model = amount;
    },
    updateState0(state, id: number) {
      const request = state.userRequests.find(req => req.id === id);
      if (request) {
        request.state = "未上传";
      }
    },
    updateState1(state, id: number) {
      const request = state.userRequests.find(req => req.id === id);
      if (request) {
        request.state = "已上传";
      }
    },
    updateState2(state, id: number) {
      const request = state.userRequests.find(req => req.id === id);
      if (request) {
        request.state = "已完成";
      }
    },
    addNewUserRequest(state) {
      const lastRequest = state.userRequests[state.userRequests.length - 1];
      const newId = lastRequest ? lastRequest.id + 1 : 1;
      const newUserRequest = {
        id: newId,
        data: '',
        model: '',
        state: '未上传',
      };
      state.userRequests.push(newUserRequest);
    },
  },
  actions: {},
  modules: {},
});
