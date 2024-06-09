<template>
  <div class="common-layout">
    <el-container>

      <el-container>
        <!-- <el-aside width="200px" class="aside">
          <CommonAside />
        </el-aside> -->
        <el-container>
          <el-header class="header" height="90px">
            <CommonHead />

          </el-header>
          <!-- <el-header class="header" height="90px">
            <LoginHead />

          </el-header> -->
          <el-main class="main">
            <img class="background-image"/>
            <div class="text-container">
              <span class="texts">这是租用模型功能的个人信息</span>
            </div>
            <div class="container">
              <div class="item">用户名: {{ $store.state.userData.username }}</div>
              <div class="item">押金金额: {{ $store.state.userData.deposit }}</div>
              <div class="item">资金金额: {{ $store.state.userData.fund }}</div>
            </div>
            <div class="buttons">
                <router-link to="/submitdeposit">
                <el-button class="large-button" size="large" type="success" round>继续</el-button>
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



</script>

<style scoped>
.large-button {
  font-size: 24px; /* 字体大小 */
  padding: 20px 40px; /* 内边距 */
  height: 80px; /* 按钮高度 */
  line-height: 1; /* 行高 */
}
.buttons {
  margin-top:80px;
  display: flex;
  justify-content: center;
  gap: 100px; 
}
.text-container {
  display: grid;
  place-items: center; /* 水平和垂直居中 */
  height: 10vh; /* 可选：根据需要调整高度 */
}
.texts {
  font-size: 30px; /* 字体大小 */
}
.background-image {
background-image: url('../images/main_bg.jpg'); /* 设置图片路径 */
background-size: cover; /* 背景图片覆盖整个元素 */
background-repeat: no-repeat; /* 背景图片不重复 */
background-position: center; /* 背景图片居中 */
width: 100%; /* 元素宽度 */
height: 84px; /* 元素高度 */
}

.container {
  flex: 1;
  overflow: auto; /* 使容器可滚动 */
  border: 1px solid #ccc;
  padding: 10px;
}

.item {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.container::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

.container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 6px;
}

.container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.container::-webkit-scrollbar-track {
  background: #f1f1f1;
}
</style>