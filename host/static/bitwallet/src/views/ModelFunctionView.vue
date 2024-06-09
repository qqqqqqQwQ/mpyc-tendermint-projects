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
            <span class="texts">请选择租用/租出模型功能</span>
            </div>
            <div class="buttons">
                <router-link to="/borrowinformation">
                <el-button class="large-button" size="large" type="success" round>租用模型</el-button>
                </router-link>
                <el-button class="large-button" size="large" type="danger" round>租出模型</el-button>
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
import { reactive } from 'vue'

// do not use same name with ref
const form = reactive({
  name: '',
})

const onSubmit = () => {
  console.log('submit!')
}
</script>
  
<style scoped>
.background-image {
background-image: url('../images/main_bg.jpg'); /* 设置图片路径 */
background-size: cover; /* 背景图片覆盖整个元素 */
background-repeat: no-repeat; /* 背景图片不重复 */
background-position: center; /* 背景图片居中 */
width: 100%; /* 元素宽度 */
height: 84px; /* 元素高度 */
}
.buttons {
  margin-top:80px;
  display: flex;
  justify-content: center;
  gap: 100px; 
}
.large-button {
  font-size: 24px; /* 字体大小 */
  padding: 20px 40px; /* 内边距 */
  height: 80px; /* 按钮高度 */
  line-height: 1; /* 行高 */
}
.text-container {
  display: grid;
  place-items: center; /* 水平和垂直居中 */
  height: 40vh; /* 可选：根据需要调整高度 */
}
.texts {
  font-size: 30px; /* 字体大小 */
}
</style>