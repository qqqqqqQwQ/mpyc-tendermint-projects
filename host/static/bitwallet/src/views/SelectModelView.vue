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
              <span class="texts">请选择数据和模型</span>
            </div>
            <div class="containers">
              <div class="container">
                <div
                  v-for="(item, index) in $store.state.dataContainer"
                  :key="index"
                  :class="{ 'item': true, 'selected': selectedIndexData === index }"
                  @click="selectData(index)"
                >
                  {{ item }}
                </div>
              </div>
              <div class="container">
                <div
                  v-for="(item, index) in $store.state.modelContainer"
                  :key="index"
                  :class="{ 'item': true, 'selected': selectedIndexModel === index }"
                  @click="selectModel(index)"
                >
                  {{ item }}
                </div>
              </div>
            </div>
            <div class="buttons">
              <router-link to="/borrowmain">
                <el-button class="large-button" type="success" round @click="updateDataModel">确认</el-button>
              </router-link>
              <router-link to="/borrowmain">
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
import { mapGetters } from 'vuex';
const { getDataContainer1, getDataContainer2 } = mapGetters(['getDataContainer1', 'getDataContainer2']);
import { useStore } from 'vuex';
const dataInput = ref(null);
const modelInput = ref(null);
const store = useStore();

const selectData = (index) => {
  selectedIndexData.value = index;
  dataInput.value = store.state.dataContainer[index];
};

const selectModel = (index) => {
  selectedIndexModel.value = index;
  modelInput.value = store.state.modelContainer[index];
};

const updateDataModel = () => {
  if(dataInput.value !== null && modelInput.value !== null)
  {
    // 创建新的 userRequest
    store.commit('addNewUserRequest');
    if (dataInput.value !== null) {
      store.commit('updateData', dataInput.value);
      dataInput.value = null;
      selectedIndexData.value = null;
    }
    if (modelInput.value !== null) {
      store.commit('updateModel', modelInput.value);
      modelInput.value = null;
      selectedIndexModel.value = null;
    }
  }
  dataInput.value = null;
  selectedIndexData.value = null;
  modelInput.value = null;
  selectedIndexModel.value = null;
};

const selectedIndexData = ref(null);
const selectedIndexModel = ref(null);

</script>
  
<style scoped>
.selected {
  background-color: red;
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
.containers {
  display: flex;
  gap: 20px; /* 容器之间的间距 */
  width: 100%;
  height: 50vh; /* 全高度 */
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