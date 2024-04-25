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
                    <el-main class="main">关于我们</el-main>
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

<style></style>