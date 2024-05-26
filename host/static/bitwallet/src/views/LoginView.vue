<template>
  <div id="login_container">
    <h3 class="login_title">
      <div id="login_head" >欢迎使用多方安全计算服务</div>
      <el-button type="default" id="register_button" @click="toRegister()">
        没有账户？点击注册
      </el-button>
    </h3>
    <el-form ref="formRef" style="max-width: 600px" :model="keyValidateForm" label-width="auto" class="demo-ruleForm"
      :rules="rules">
      <el-form-item label="用户名" prop="username" id="usernameForm" style="width: 90%">
        <el-input v-model="keyValidateForm.username"  autocomplete="off"
          placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码" prop="password" id="passwordForm" style="width: 90%">
        <el-input v-model="keyValidateForm.password" type="password" show-password autocomplete="off"
          placeholder="请输入密码" />
      </el-form-item>
      <div id="service_rules" style="color: #333">登录表示您已同意<a href="https://baidu.com" style="color: #330362" target="_blank">《服务条款》</a></div>
      <el-form-item id="login_button_container">
        <el-button type="primary" id="login_button" plain @click="Login(formRef)">登录</el-button>
        <el-button @click="resetForm(formRef)" plain type="info" id="reset_button">重置</el-button>
      </el-form-item>

    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, LAST_KEYS } from 'element-plus';
import axios from 'axios';

//定义表单数据接口
interface LoginForm {
  username: string,
  password: string,
}
//使用useRouter获取路由实例
const router = useRouter();
// 创建一个引用ref对象来存储表单实例
const formRef = ref<FormInstance>()
// 创建一个响应式对象来存储需要验证的表单数据
const keyValidateForm = reactive<LoginForm>({
  username: '',
  password: '',
})
// 创建用于校验的规则对象
const rules = reactive({
  username: [
    { required: true, message: '请输入你的用户名', trigger: 'blur' },
    { min: 5, max: 20, message: '账户不能为空', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入你的密码', trigger: 'blur' },
    { min: 5, max: 20, message: '长度应该在5到20之间', trigger: 'blur' },
  ]
});
// 定义登录函数，通过formEl参数进行表单校验并提交登录请求
const Login = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate((valid, fields) => {
    if (valid) {
      // 此处应该进行登录请求，暂时注释掉
      // axios.post('http://localhost:3312/sys-user/login ',ruleForm).then((resp)=>{
      //     let data=resp.data;
      //     if(data.success) {

      //     }
      // })
      // 输出登录成功信息，重置表单并路由跳转到首页
      console.log('login!', keyValidateForm);
      formEl.resetFields()
      ElMessage({
        message: '成功登录！',
        type: 'success',
      })
      router.push({ path: '/' });
    }
    else {

      console.log('error login!', fields);
      ElMessage({
        message: '登陆失败！',
        type: 'error',
      })
    }
  })
}

// 重置表单的方法，接受一个表单实例作为参数
const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  // 调用表单实例的resetFields方法重置表单
  formEl.resetFields()
  ElMessage('重置成功')
}
const toRegister = () => {
  router.push({ path: '/register' });
}
</script>

<style scoped>
#login_button {
  width: 23%;
  font-size: 14px;
  margin-left: auto;
}

#reset_button {
  width: 23%;
  font-size: 14px;
  margin-right: auto;
}

#login_head {
  font-size: 27px;
  color: #333;
  margin-bottom: 5px;

}

#login_subhead {
  font-size: 16px;
  color: #282727d7;
}

#login_container {
  border-radius: 15px;
  margin: 4% auto;
  width: 475px;
  height: 275px;
  background: #fff;
  border: 1px solid #eaeaea;
  box-shadow: 0 0 20px #8a8d8ec9;
  padding: 20px 10px 40px 28px;
  justify-content: center;
  align-items: center;
  position: relative;
}


.login_title {
  text-align: center;
  margin-top: 5px;

}

#register_button {
  width: 40%;
  height: 200%;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  margin-top: 8px;
  font-size: 13px;
}

#service_rules {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  margin-bottom: 20px;
}
</style>