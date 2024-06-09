<template>
  <div class="common-layout">
    <el-container>

      <el-container>
        <!-- <el-aside width="200px" class="aside">
          <CommonAside />
        </el-aside> -->
        <el-container>
<!--          <el-header class="header" height="90px">-->
<!--            <CommonHead />-->

<!--          </el-header>-->
          <el-header class="header" height="90px">
            <LoginHead />

          </el-header>
          <el-main class="main">
            <img class="background-image"/>
            <img class="info_image" src="../images/main_info.jpg" alt="Element logo" />
            <div class="buttons">
              <el-button type="primary" size="large" round>数据学习</el-button>
              <el-button type="info" size="large" round>联邦管理</el-button>
              <router-link to="/modelfunction">
                <el-button type="warning" size="large" round>模型租用</el-button>
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

<style>
.background-image {
  background-image: url('../images/main_bg.jpg'); /* 设置图片路径 */
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-repeat: no-repeat; /* 背景图片不重复 */
  background-position: center; /* 背景图片居中 */
  width: 100%; /* 元素宽度 */
  height: 84px; /* 元素高度 */
}
.info_image{
  width: 100%; 
  height: 75%;
}
.buttons {
  display: flex;
  justify-content: center;
  gap: 100px; 
}
</style>