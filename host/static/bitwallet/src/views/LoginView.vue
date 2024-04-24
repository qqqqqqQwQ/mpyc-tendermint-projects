<template>
  <div id="login_container">
    <h3 class="login_title">
      <div id="login_head">欢迎使用多方安全计算服务</div>
      <div id="login_subhead">请输入你的公钥</div>
    </h3>
    <el-form
      ref="formRef"
      style="max-width: 600px"
      :model="keyValidateForm"
      label-width="auto"
      class="demo-ruleForm"
      :rules="rules"

    >
      <el-form-item
        label="public-key"
        prop="publickey"
        id="publickeyForm"
      >
        <el-input
            v-model="keyValidateForm.publickey"
            type="text"
            autocomplete="off"
            placeholder="点此输入"
          />
      </el-form-item>
      <el-form-item id="login_button_container">
        <el-button type="primary" id="login_button" plain @click="Login(formRef)">登录</el-button>
        <el-button @click="resetForm(formRef)"  plain type ="info" id="reset_button"  >重置</el-button>
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
  interface LoginForm{
    publickey:string
  }
  //使用useRouter获取路由实例
  const router = useRouter();
  // 创建一个引用ref对象来存储表单实例
  const formRef = ref<FormInstance>()
  // 创建一个响应式对象来存储需要验证的表单数据
  const keyValidateForm = reactive<LoginForm>({
    publickey: '',
  })
  // 创建用于校验的规则对象
  const rules = reactive<FormRules<LoginForm>>({
      publickey: [
          { required: true, message: '请输入你的公钥', trigger: 'blur' },
          { min: 5, max: 20, message: '长度应该在5到20之间', trigger: 'blur' },
      ]
  })
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
              console.log('login!',keyValidateForm);
              formEl.resetFields()
              ElMessage({
                  message: '成功登录！',
                  type: 'success',
              })
              router.push({ path: '/home' });
          } 
          else {
              console.log('error login!', fields)
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
</script>

<style scoped>
    #login_button{
      width:24%;
      font-size:14px;
      margin-left: auto;    
    }
    #reset_button{
      width:24%;
      font-size:14px;
      margin-right: auto;    
    }
    #login_head{
      font-size:22px;
      color: #333;
      margin-bottom: 5px;
      
    }
    #login_subhead{
      font-size:16px; 
      color: #282727d7;
    }
    #login_container{
      border-radius:15px;
      margin:10% auto;
      width:350px;
      height:45%;
      background:#fff;
      border:1px solid #eaeaea;
      box-shadow:0 0 20px #8a8d8ec9;
      padding:20px 20px 20px 28px;
      justify-content: center;
      align-items: center;
      position: relative;
    }
    #login_button_container{
      margin-bottom: 10px;
      margin-top: 25px;

    }
    .login_title{
      text-align: center;
      margin-top: 5px;

    }
    

</style>