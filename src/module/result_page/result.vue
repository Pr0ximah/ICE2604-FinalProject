<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElMenu, ElMenuItem, ElRow, ElCol, ElFooter, ElText } from 'element-plus';
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import LOGO from "@/assets/LOGO_S.png"
import LOGO_L from "@/assets/LOGO.png"
import API from '../../components/axios_instance'

let datalist = ref()
let result_total_num = ref(0)
const size_per_page = ref(20)   // 每页显示的条目数

function getQueryContent(name) {
    let reg = new RegExp(name + '=.*&?')
    let r = window.location.search.match(reg)
    if (r != null) {
        console.log(decodeURI(r))
        return decodeURI(r).split('=')[1]
    }
}

const content = ref(getQueryContent('search'))

function get() {
    API({
        url: `/data_proxy/data`,
        method: 'get'
    }).then((e) => {
        datalist.value = e['data']['data']
        result_total_num = datalist.value.length
    }).catch(() => {
    })
}

function gotoLink(url) {
    console.log(url)
    window.open(url, "_blank")
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
                <ElMenu mode="horizontal" :ellipsis="false" style="width: 100%;" ref="menu">
                    <ElMenuItem :index="0" @click="backToHome">
                        <ElImage class="left-menu-logo" :src="LOGO" fit="contain" />
                    </ElMenuItem>
                    <div style="flex-grow: 1;" />
                    <ElRow style="align-items: center; width: 20%; margin-right: 2%" justify="center">
                        <ElCol :span="2" justify="center">
                            <el-icon style="padding-top: 2px; padding-right: 12px; transform: scale(1.1); float: right">
                                <Search />
                            </el-icon>
                        </ElCol>
                        <ElCol :span="22">
                            <ElInput v-model="content" style="height: 30px;"></ElInput>
                        </ElCol>
                    </ElRow>
                </ElMenu>
            </ElContainer>
        </ElHeader>
        <ElMain class="result">
            <ElRow style="width: 100%;" :gutter="80">
                <ElCol :span="4">
                    left
                    <div>
                        <ElButton class="default" @click="get" style="margin-top: 20px;"> press </ElButton>
                    </div>
                </ElCol>
                <ElCol :span="16">
                    <ElCard shadow="hover" v-for="data in datalist" style="margin: 20px 20px 20px 20px; padding: 10px 10px 10px 10px;">
                        <div style="margin: 10px 5px 10px 5px;">title = {{ data["title"] }}</div>
                        <div style="margin: 10px 5px 10px 5px;">year = {{ data["year"] }}</div>
                        <div style="margin: 30px 5px 10px 5px;" v-if="data['link'] && data['link'] !== ''">
                            <ElButton style="default" @click="gotoLink(data['link'])"> link </ElButton>
                        </div>
                    </ElCard>
                    <el-pagination layout="prev, pager, next" :total="result_total_num" hide-on-single-page="true" :page-size="size_per_page"/>
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
