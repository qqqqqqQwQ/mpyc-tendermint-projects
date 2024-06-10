<template>
  <div id="register_container">
    <h3 class="register_title">
      <div id="register_head" >注册属于你的账户</div>
    </h3>
    <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" status-icon :rules="rules" label-width="auto" class="demo-ruleForm">
      <el-form-item label="用户名" prop="username">
      <el-input v-model="ruleForm.username"  style="width: 90%" placeholder="请输入用户名"/>
      </el-form-item>
      <el-form-item label="密码" prop="pass">
      <el-input v-model="ruleForm.pass" type="password" autocomplete="off" style="width: 90%"  placeholder="请输入密码"/>
      </el-form-item>
      <el-form-item label="确认密码" prop="checkPass">
        <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" style="width: 90%" placeholder="请再次输入密码"/>
      </el-form-item>
      <div id="service_rules">已有账号？<router-link to="/login">立即登录</router-link></div>
      <el-form-item >
        <el-button type="primary" plain @click="submitForm(ruleFormRef)" id="register_button">注册</el-button>
        <el-button @click="resetForm(ruleFormRef)"  type="info" plain id="reset_button">重置</el-button>
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
import { useStore } from 'vuex';
const router = useRouter();
const ruleFormRef = ref<FormInstance>()
const store = useStore();
const checkusername = (rule: any, value: any, callback: any) => {
  // if (!value) {
  //   return callback(new Error('Please input the username'))
  // }
  // setTimeout(() => {
  //   if (!Number.isInteger(value)) {
  //     callback(new Error('Please input digits'))
  //   } else {
  //     if (value < 18) {
  //       callback(new Error('username must be greater than 18'))
  //     } else {
  //       callback()
  //     }
  //   }
  // }, 1000)
  callback()
}

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please input the password'))
  } else {
    if (ruleForm.checkPass !== '') {
      if (!ruleFormRef.value) return
      ruleFormRef.value.validateField('checkPass')
    }
    callback()
  }
}
const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== ruleForm.pass) {
    callback(new Error("两次输入的密码不一致！"))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  username: '',
  pass: '',
  checkPass: ''

})

const rules = reactive<FormRules<typeof ruleForm>>({
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
  username: [{ validator: checkusername, trigger: 'blur' }],
})

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
       axios.post('http://localhost:3000/users', {
        username: ruleForm.username,
        password: ruleForm.pass
      })
      .then((response) => {
        // 请求成功的处理
        console.log(response);
        ElMessage({
        message: '成功注册！',
        type: 'success',
      })
        store.commit('updateUsername', ruleForm.username);
        router.push({path: '/loginhome'});
      })
      .catch((error) => {
        // 请求失败的处理
        console.error(error);
        ElMessage({
        message: '注册失败！',
        type: 'error',
      })

      });
    } else {
      console.log('error submit!')

    }
  })
}

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style scoped>

#register_button{
  width: 23%;
  font-size: 14px;
  margin-left: auto;

}
#reset_button {
  width: 23%;
  font-size: 14px;
  margin-right: auto;
}


#register_head {
  font-size: 25px;
  color: #333;
  margin-bottom: 5px;

}

#register_subhead {
  font-size: 16px;
  color: #282727d7;
}

#register_container {
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


.register_title {
  text-align: center;
  margin-top: 5px;
  margin-bottom: 30px;

}


#service_rules {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  margin-bottom: 20px;
}
</style>

<style scoped>

</style>