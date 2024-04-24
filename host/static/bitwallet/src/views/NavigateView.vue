<template>
  <div>
    <h1 :msg="msg">{{ msg }}</h1>
    <HelloWorld :msg="msg" />
    <input v-model="msg" type="text" />
  </div>
</template>

<script lang="ts" scoped>
import { defineComponent, onMounted, ref } from 'vue';
import HelloWorld from "@/components/HelloWorld.vue";
export default defineComponent({
  // 需要启用子组件作为模板
  components: {
    HelloWorld,
  },


  // 定义一些数据并 `return` 给 `<template />` 用
  setup() {
    // 使用 ref 创建响应式变量
    const msg = ref("Welcome to BitWallet!");

    // 不要忘记 `return` ，否则 `<template />` 拿不到数据
    return {
      msg,
    }
  },
})

</script>

<style></style>