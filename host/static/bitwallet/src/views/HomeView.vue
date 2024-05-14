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
            <el-row class="rows">
              <el-col class="cols_left">我们的价值主张</el-col>
              <el-col class="cols_right">我们的独特技术</el-col>
            </el-row>
            <el-row class="rows">
              <el-col class="cols_left">数据隐私保护的高度可信性</el-col>
              <el-col class="cols_right">使用Tendermint搭建区块链</el-col>
            </el-row>
            <el-row class="rows">
              <el-col class="cols_left">去中心化的安全保障机制</el-col>
              <el-col class="cols_right">使用MPyC框架设计多方安全协议</el-col>
            </el-row>
            <el-row class="rows">
              <el-col class="cols_left">数据共享和模型融合的高效性</el-col>
              <el-col class="cols_right">使用PySyft框架用于搭建联邦学习</el-col>
            </el-row>
          </el-main>
          <el-footer class="Footer">Footer</el-footer>
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
.rows{
  width:100%;
  text-align: center;
  display: block;
}
.cols_left{
  width:50%;
  text-align: center;
  float:left;
  display: block;
}
.cols_right{
  width:50%;
  text-align: center;
  float:right;
  display: block;
}
</style>