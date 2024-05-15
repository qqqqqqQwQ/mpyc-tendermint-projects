<template>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :ellipsis="false"
        @select="handleSelect">
        <el-menu-item index="0">
            <img style="width: 90px; height: 90px" src="@/images/SMPC.png" alt="Element logo" />
        </el-menu-item>
        <div class="flex-grow" />

        <td class="line">
        </td>
        <td class="line">
            <div class="dashed" />
        </td>
        <el-menu-item @click="clickMenu(item)" v-for="item in noChildren" :key="item.name" :index="item.name">
            <el-icon><home-filled /></el-icon>
            <template #title>{{ item.label }}</template>
        </el-menu-item>

        <el-menu-item @click="clickMenu(item)" v-for=" item in eInfo" :key="item.name" :index="item.name">
            <el-icon>
                <Avatar />
            </el-icon>
            <template #title>{{ item.label }}</template>
        </el-menu-item>

        <el-menu-item @click="clickMenu(item)" v-for=" item in aboutUsMenu" :key="item.name" :index="item.name">
            <el-icon>
                <Promotion />
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

        <el-button type="primary" size="large" plain @click="clickLogin()">登录</el-button>
        <el-button type="default" size="large" plain @click="clickRegister()">注册</el-button>
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
    Promotion,
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
const clickLogin = () => {
    router.push("/login")
}
const clickRegister = () => {
    router.push("/register")
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
                path: "/testone",
                name: "TestOne",
                component: () => import("@/views/TestOneView.vue"),
                label: "测试一路由",

            },
            {
                path: "/testtwo",
                name: "TestTwo",
                component: () => import("@/views/TestTwoView.vue"),
                label: "测试二路由",
            },
        ],
    }
])

const evaluationInfo = ref([{
    path: "/evaluation",
    name: "evaluation",
    label: "贷款信息评估",
    component: () => import("@/views/EvaluationView.vue")
}])

const settingMenuData = ref([
    {
        path: "/setting",
        name: "setting",
        label: "设置",
        component: () => import("@/views/SettingView.vue"),
    }
])

const aboutUsData=ref([
    {
        path: "/aboutus",
        name: "aboutus",
        label:"关于我们",
        component: () => import("@/views/AboutUs.vue"),
    }
])
const aboutUsMenu = computed(() => {
    return aboutUsData.value;
});
const settingMenu = computed(() => {
    return settingMenuData.value;
});
const eInfo = computed(() => {
    return evaluationInfo.value;
});
// 没有子菜单的
const noChildren = computed(() => {
    return menuData.value.filter(item => !item.children);
});

// 有子菜单的
const hasChildren = computed(() => {
    return menuData.value.filter(item => item.children);
});

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
}
</script>

<style>
.flex-grow {
    flex-grow: 1;
}
.el-menu{
    height:100%;
    align-items:center;
}
.el-button{
    margin-left:10px;
    margin-right:10px;

}

</style>