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
            <img class="background-image" />
            <el-table :data="tableData" style="width: 100%" class="table-container">
              <el-table-column fixed prop="id" label="编号" width="150" />
              <el-table-column prop="data" label="数据" width="120" />
              <el-table-column prop="model" label="模型" width="120" />
              <el-table-column prop="state" label="当前状态" width="120" />
              <el-table-column fixed="right" label="操作" width="240">
                <template #default="{ row }">
                  <div class="button-group">
                    <el-button type="success" size="large" round @click="uploadClick(row.id)">上传请求</el-button>
                    <el-button type="danger" size="large" round @click="downloadClick(row.id)">下载结果</el-button>
                  </div>
                </template>
              </el-table-column>
            </el-table>
          </el-main>
          <el-footer class="Footer"></el-footer>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts" setup>
import { defineComponent, onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import CommonAside from "@/components/CommonAside.vue";
import CommonHead from "@/components/CommonHeader.vue";
import LoginHead from "@/components/LoginHeader.vue";
import { ElMessage } from 'element-plus';

const store = useStore();
const uploadClick = (id: number) => {
  const request = store.state.userRequests.find(req => req.id === id);
  if (request && request.state !== "未上传") {
    ElMessage({
      message: '已经上传请求,请勿重复上传!',
      type: 'warning',
    });
  } else {
    store.commit('updateState1', id);
    ElMessage({
      message: '上传请求成功!',
      type: 'success',
    });

    // 设置一个定时器，在指定时间后执行
    setTimeout(() => {
      store.commit('updateState2', id);
      ElMessage({
        message: '请求已完成!',
        type: 'success',
      });

      // 在定时器完成后修改 deposit 和 fund
      store.commit('updateDeposit', store.state.depositModified);
      store.commit('updateFund', store.state.fundModified);
    }, 5000); // 模拟承包商在X秒后完成参与方的请求,X默认为5000毫秒,可修改
  }
}


const downloadFile = () => {
  const fileUrl = process.env.BASE_URL + 'loan_predication_test.csv'; // 构建文件的 URL路径,我放在public文件夹里面了,可修改

  // 创建一个链接元素
  const link = document.createElement('a');
  link.href = fileUrl;
  link.download = 'loan_predication_test.csv'; // 设置下载文件的名称,可修改
  link.style.display = 'none';

  // 将链接元素添加到 DOM 中
  document.body.appendChild(link);

  // 触发点击事件
  link.click();

  // 删除链接元素
  document.body.removeChild(link);
};



const downloadClick = (id: number) => {
  const request = store.state.userRequests.find(req => req.id === id);
  if (request && request.state !== "已完成") {
    ElMessage({
      message: '请求尚未完成,请耐心等待!',
      type: 'warning',
    });
  } else {
    ElMessage({
      message: '开始下载计算结果!',
      type: 'success',
    });
    downloadFile();
  }
}

const tableData = ref([]);

onMounted(() => {
  tableData.value = store.state.userRequests.filter(request => request.id !== 0);
});
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

.table-container {
  margin-top: 50px;
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: calc(100vh - 180px); /* 根据header和footer的高度调整 */
}

.button-group {
  display: flex;
  gap: 5px; /* 按钮之间的间距 */
}
</style>
