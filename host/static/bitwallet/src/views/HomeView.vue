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
            <div class="background-image">
            </div>
            <div class="background-color">
              <el-col class="cols_top"></el-col>
              <el-col class="cols_left">我们的价值主张</el-col>
              <el-col class="cols_right">我们的独特技术</el-col>
              <el-col class="cols_left">数据隐私保护的高度可信性</el-col>
              <el-col class="cols_right">使用Tendermint搭建区块链</el-col>
              <el-col class="cols_left">去中心化的安全保障机制</el-col>
              <el-col class="cols_right">使用MPyC框架设计多方安全协议</el-col>
              <el-col class="cols_left">数据共享和模型融合的高效性</el-col>
              <el-col class="cols_right">使用PySyft框架用于搭建联邦学习</el-col>
              <el-col class="cols_bottom"></el-col>
            </div>
            <img class="arrows_image" src="../images/arrows.jpg" alt="Element logo" />
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
.background-color {
  background-color:aqua;
  background-size: cover; /* 背景图片覆盖整个元素 */
  background-repeat: no-repeat; /* 背景图片不重复 */
  background-position: center; /* 背景图片居中 */
  width: 100%; /* 元素宽度 */
  height: 84px; /* 元素高度 */
}
.cols_top{
  width:100%;
  border-top: 1px solid black;
  z-index:10;
}
.cols_bottom{
  width:100%;
  margin-top:82px;
  border-bottom: 1px solid black;
  z-index:10;
}
.cols_left{
  width:48%;
  text-align: center;
  float:left;
  display: block;
  font-size:16px;
  border-left: 1px solid black;
  color:white;
  z-index:10;
}
.cols_right{
  width:48%;
  text-align: center;
  float:right;
  display: block;
  font-size:16px;
  border-right: 1px solid black;
  color:white;
  z-index:10;
}
.arrows_image{
  width: 100%; 
  height: 75%;
}
</style>