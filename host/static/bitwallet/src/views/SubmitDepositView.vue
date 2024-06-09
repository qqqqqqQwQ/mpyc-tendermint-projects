<template>
  <div class="common-layout">
    <el-container>

      <el-container>
        <!-- <el-aside width="200px" class="aside">
          <CommonAside />
        </el-aside> -->
        <el-container>
          <!-- <el-header class="header" height="90px">
            <CommonHead />

          </el-header> -->
          <el-header class="header" height="90px">
            <LoginHead />

          </el-header>
          <el-main class="main">
            <img class="background-image"/>
            <div class="text-container">
              <span class="texts">请提交押金</span>
            </div>
            <div class="input-container">
              <input type="number" v-model="depositInput" placeholder="请输入押金金额" class="custom-input">
            </div>
            <div class="buttons">
              <router-link to="/selectmodel">
                <el-button class="large-button" type="success" round @click="updateDeposit">确认</el-button>
              </router-link>
              <router-link to="/selectmodel">
                <el-button class="large-button" type="danger" round>跳过</el-button>
              </router-link>
            </div>
          </el-main>
          <el-footer class="Footer"></el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { defineComponent, onMounted, ref } from 'vue';
import CommonAside from "@/components/CommonAside.vue";
import CommonHead from "@/components/CommonHeader.vue";
import LoginHead from "@/components/LoginHeader.vue";
import { useStore } from 'vuex';
// 在组件挂载后获取 store 对象
let store;
onMounted(() => {
  store = useStore(); // 在生命周期钩子中使用 useStore() 获取 $store 对象
});

const depositInput = ref(null);

// 定义更新押金的函数
const updateDeposit = () => {
  if (depositInput.value !== null) {
    store.commit('updateDeposit', depositInput.value);
    depositInput.value = null; // 清空输入框
  }
};

</script>

<style scoped>
.input-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 40vh; /* 设置容器高度为视口高度，实现垂直居中 */
}

.custom-input {
  width: 300px; /* 设置输入框宽度 */
  height: 40px; /* 设置输入框高度 */
  text-align: center; /* 文本居中 */
  font-size: 16px; /* 字体大小 */
}

.text-container {
  display: grid;
  place-items: center; /* 水平和垂直居中 */
  height: 10vh; /* 可选：根据需要调整高度 */
}
.texts {
  font-size: 30px; /* 字体大小 */
}
.large-button {
  font-size: 24px; /* 字体大小 */
  padding: 20px 40px; /* 内边距 */
  height: 80px; /* 按钮高度 */
  line-height: 1; /* 行高 */
}
.buttons {
  display: flex;
  justify-content: center;
  gap: 100px; 
}
.background-image {
  background-image: url('../images/main_bg.jpg'); /* 设置图片路径 */
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-repeat: no-repeat; /* 背景图片不重复 */
  background-position: center; /* 背景图片居中 */
  width: 100%; /* 元素宽度 */
  height: 84px; /* 元素高度 */
}
</style>