<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElMenu, ElMenuItem, ElRow, ElCol, ElFooter, ElText } from 'element-plus';
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import LOGO from "@/assets/LOGO_S.png"
import LOGO_L from "@/assets/LOGO.png"
import API from '../../components/axios_instance'

const content = ref("")
let datalist = ref()

function getQueryContent(name) {
    let reg = new RegExp(name + '=.*&?')
    let r = window.location.search.match(reg)
    if (r != null) {
        console.log(decodeURI(r))
        return decodeURI(r).split('=')[1]
    }
}

function get() {
    API({
        url: `/data_proxy/data`,
        method: 'get'
    }).then((e)=>{
        datalist.value = e['data']['data']
        console.log(datalist.value)
    }).catch(()=>{
    })
}

const searchVal = ref(getQueryContent("search"))

function backToHome() {
    window.open("../../../", "_self")
}
</script>

<template>
    <ElContainer style="height: 100%; height: 100%;">
        <ElHeader>
            <ElContainer>
                <ElMenu mode="horizontal" :ellipsis="false" style="width: 100%;">
                    <ElMenuItem :index="0" @click="backToHome">
                        <ElImage class="left-menu-logo" :src="LOGO" fit="contain" />
                    </ElMenuItem>
                    <div style="flex-grow: 1;" />
                    <ElRow style="align-items: center; width: 20%; padding-right: 20px" justify="center">
                        <ElCol :span="2" justify="center">
                            <el-icon style="padding-top: 2px; padding-right: 12px; transform: scale(1.1); float: right">
                                <Search />
                            </el-icon>
                        </ElCol>
                        <ElCol :span="22">
                            <ElInput v-model="content" style="height: 30px;"></ElInput>
                        </ElCol>
                    </ElRow>
                    <ElMenuItem>
                        <ElText> 关于我们 </ElText>
                    </ElMenuItem>
                </ElMenu>
            </ElContainer>
        </ElHeader>
        <ElMain class="result">
            <ElRow style="width: 100%;" :gutter="80">
                <ElCol :span="4">
                    left
                    <div><ElButton class="default" @click="get" style="margin-top: 20px;"> press </ElButton></div>
                </ElCol>
                <ElCol :span="16">
                    <ElCard shadow="hover" v-for="data in datalist" style="margin: 20px 20px 20px 20px">
                        <div style="margin: 5px 5px 5px 5px;">title={{ data["title"] }}</div>
                        <div style="margin: 5px 5px 5px 5px;">id={{ data["id"] }}</div>
                    </ElCard>
                </ElCol>
                <ElCol :span="4">
                    right
                </ElCol>
            </ElRow>
            <!-- 回到顶部 -->
            <!-- <el-backtop :right="100" :bottom="180" /> -->
        </ElMain>
        <ElFooter>
            <ElImage class="bottom-logo" :src="LOGO_L" fit="contain"
                style="height: 70%; margin: 20px 0px 25px 0px; margin-left: 3%; width: auto;" />
            <div
                style="float:right; height: 100%; display: flex; align-items: center; justify-content: center; padding-right: 3%;">
                <ElCol>
                    <ElRow class="bottom-des-row">
                        <ElText size="large"> IE Search </ElText>
                    </ElRow>
                    <ElDivider style="margin-top: 10px; margin-bottom: 10px;" />
                    <ElRow class="bottom-des-row">
                        <ElText> SJTU Course ICE2604 </ElText>
                    </ElRow>
                    <ElRow class="bottom-des-row">
                        <ElText> Final Project </ElText>
                    </ElRow>
                    <ElRow class="bottom-des-row">
                        <ElText> © Course Group 10 </ElText>
                    </ElRow>
                </ElCol>
            </div>
        </ElFooter>
    </ElContainer>
</template>
