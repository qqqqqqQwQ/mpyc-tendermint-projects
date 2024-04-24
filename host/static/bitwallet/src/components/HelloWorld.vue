<!-- Template 代码和 Vue 2 一样 -->
<template>
  <p class="msg">{{ msg }}</p>
</template>

<!-- Script 代码需要使用 Vue 3 的新写法-->
<script lang="ts">
// Vue 3 的 API 需要导入才能使用
import { defineComponent } from 'vue'
  export default defineComponent({
    props: {
      msg:String,
    },
      // 在这里需要添加一个入参
  setup(props) {
    // 该入参包含了当前组件定义的所有 props
    console.log(props)
  },


})
</script>

<!-- CSS 代码和 Vue 2 一样 -->
<style scoped>
.msg {
  font-size: 14px;
}
</style>