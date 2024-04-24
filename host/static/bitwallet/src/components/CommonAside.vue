<template>

    <el-menu default-active="2" class="el-menu-vertical-demo" :collapse="isCollapse" active-text-color="#ffd04b"
        text-color="#ffffff" background-color="#409eff" @open="handleOpen" @close="handleClose">

        <h3 class="menutitle">logo或者网站名称</h3>
        <td class="line">
        </td>
        <td class="line">
            <div class="dashed" />
        </td>
        <el-menu-item @click="clickMenu(item)" v-for="item in noChildren" :key="item.name" :index="item.name">
            <el-icon><home-filled /></el-icon>
            <template #title>{{ item.label }}</template>
        </el-menu-item>

        <el-menu-item @click="clickMenu(item)" v-for=" item in personInfo" :key="item.name" :index="item.name">
            <el-icon>
                <Avatar />
            </el-icon>
            <template #title>{{ item.label }}</template>
        </el-menu-item>

        <el-sub-menu v-for="item in hasChildren" :key="item.name" index="item.name">
            <template #title>
                <el-icon>
                    <location />
                </el-icon>
                <span>{{ item.label }}</span>
            </template>
            <el-menu-item-group @click="clickMenu(subItem)" v-for="subItem in item.children" :key="subItem.name">
                <el-menu-item index="subItem.name">{{ subItem.label }}</el-menu-item>
            </el-menu-item-group>
        </el-sub-menu>


        <el-menu-item @click="clickMenu(item)" v-for="item in settingMenu" :key="item.name" :index="item.name">
            <el-icon>
                <Setting />
            </el-icon>
            <template #title>{{ item.label }}</template>
        </el-menu-item>


    </el-menu>

</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { ref, computed } from 'vue'
import {
    Document,
    Menu as IconMenu,
    Location,
    Setting,
    Comment,
    HomeFilled,
    Avatar,
} from '@element-plus/icons-vue'
//使用useRouter获取路由实例
const router = useRouter();
const isCollapse = ref(false)
const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
const clickMenu = (item: any) => {
    console.log(item)
    router.push(item.path)
}
const menuData = ref([
    {
        path: "/",
        name: "home",
        component: () => import("@/views/HomeView.vue"),
        label: "首页",
    },
    {
        path: "/main",
        name: "main",
        component: import("@/views/NavigateView.vue"),
        // 注意：这里是二级路由，在 `path` 的前面没有 `/`
        label: "导航",
        children: [
            {
                path: "/main/testone",
                name: "TestOne",
                component: () => import("@/views/TestOneView.vue"),
                label: "测试一路由",

            },
            {
                path: "/main/testtwo",
                name: "TestTwo",
                component: () => import("@/views/TestTwoView.vue"),
                label: "测试二路由",
            },
        ],
    }
])

const personInfo = ref([{
    path: "/personinfo",
    name: "personinfo",
    label: "个人信息",
    component: () => import("@/views/PersonInfoView.vue"),
}])

const settingMenuData = ref([
    {
        path: "/setting",
        name: "setting",
        label: "设置",
        component: () => import("@/views/SettingView.vue"),
    }
])

const settingMenu = computed(() => {
    return settingMenuData.value;
});
const Info = computed(() => {
    return personInfo.value;
});
// 没有子菜单的
const noChildren = computed(() => {
    return menuData.value.filter(item => !item.children);
});

// 有子菜单的
const hasChildren = computed(() => {
    return menuData.value.filter(item => item.children);
});
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
}

.el-menu {
    height: 100vh;
    overflow: hidden;
    text-align: center;
    justify-content: center;
    position: relative;
    border:0px;
}

.menutitle {
    color: #fff;
    line-height: 48px;
    font-weight: 600;
}

.line {
    height: 2px;
    width: 200px;
    color:#fff;
    background-color: #fff;
    margin-bottom: 30px;
    border-top: 1px solid;
    overflow: hidden;
}
</style>
