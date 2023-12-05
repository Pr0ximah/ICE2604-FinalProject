<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElMenu, ElMenuItem, ElRow, ElCol, ElFooter, ElText, ElCheckboxGroup } from 'element-plus';
import { ElMessage } from 'element-plus';
import { onMounted, reactive, ref, watch, onBeforeMount } from 'vue'
import { Search, Calendar, User, Star } from '@element-plus/icons-vue'
import LOGO from "@/assets/LOGO_S.png"
import LOGO_L from "@/assets/LOGO.png"
import API from '../../components/axios_instance'
import chart from '../../components/echarts/chart.vue'

let chartYear = ref()
let datalist = ref()
let datalistAll = ref()
let childData = ref()
let result_total_num = ref(0)
const size_per_page = ref(15)   // 每页显示的条目数
let emptyResult = ref(true)
let searchOptionVal = ref("")
let currentPage = ref(1)
let filterYearList = ref([{"year": 1991, "num": 1}])
const filterYearCheckList = ref([])

function getQueryContent(name) {
    let reg = new RegExp(name + '=([^&]*)')
    let r = window.location.search.match(reg)
    if (r != null) {
        return decodeURI(r[0]).split('=')[1]
    }
}

const content = ref(getQueryContent('content'))
const enableAll = ref(false)

function get() {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    API({
        url: base + `/search/content=${getQueryContent('content')}&type=${getQueryContent('type')}`,
        method: 'get'
    }).then((e) => {
        datalistAll.value = e['data']['data']
        result_total_num = datalistAll.value.length
        childData.value = datalistAll.value
        emptyResult = (result_total_num == 0)
        const type = getQueryContent('type')
        if (searchOptionVal.value != type) {
            searchOptionVal.value = type
        }
        switchPage()
    }).catch(() => {
    }).then(() => {
        chartYear.value.init()
    })
}

function switchPage() {
    let start = (currentPage.value - 1) * size_per_page.value
    let end = currentPage.value * size_per_page.value
    if (end >= result_total_num) {
        end = result_total_num
    }
    datalist.value = datalistAll.value.slice(start, end)
}

watch(currentPage, () => {
    switchPage()
    window.scrollTo({
        top: 0
    })
})

function gotoLink(url) {
    window.open(url, "_blank")
}

function convertList(lists) {
    let res = ""
    for (var i = 0; i < lists.length; i++) {
        res += lists[i]
        res += ", "
    }
    return res.slice(0, -2)
}

const searchVal = ref(getQueryContent("search"))

function backToHome() {
    window.open("./", "_self")
}

const SearchOption = [
    {
        value: 'Title'
    },
    {
        value: 'Year'
    },
    {
        value: 'Author'
    },
    {
        value: 'Keywords'
    }
]

function search() {
    if (!content.value) {
        ElMessage("输入为空")
        return
    } else {
        if (searchOptionVal.value === "Year" && !/^[0-9]*$/.test(content.value)) {
            ElMessage("年份必须为数字")
            return
        }
        gotoResult()
    }
}

function gotoResult() {
    window.open(`/search.html?content=${content.value}&type=${searchOptionVal.value}`, "_self")
}

onBeforeMount(() => {
    get()
})

onMounted(() => {
    chartYear.value.init()
})
</script>

<template>
    <ElContainer class="bg-all" style="height: 100%; height: 100%;">
        <ElHeader>
            <ElContainer>
                <ElMenu mode="horizontal" :ellipsis="false" style="width: 100%;" ref="menu">
                    <ElMenuItem :index="0" @click="backToHome">
                        <ElImage class="left-menu-logo" :src="LOGO" fit="contain" />
                    </ElMenuItem>
                </ElMenu>
            </ElContainer>
        </ElHeader>
        <ElMain class="result">
            <ElRow style="width: 100%;" :gutter="30">
                <ElCol :span="3" style="height: 100vh">
                    <ElCard class="preset1" style="margin-top: 10%; width: 100%;">
                        <div style="text-align: center;">
                            <ElText style="font-size: medium; text-align: center;">filter</ElText>
                        </div>
                        <ElDivider border-style="dashed" style="margin-top: 15px; margin-bottom: 15px;"></ElDivider>
                        <div style="margin-left: 6%;">
                            <div style="margin-bottom: 5px;">
                                <ElText>Year</ElText>
                            </div>
                            <ElCheckboxGroup v-model="filterYearCheckList" @change="console.log(filterYearCheckList)">
                                <ElCheckbox v-for="year in filterYearList" :label="year['year']">
                                    <div style="font-size: small;" @click="console.log(year['year'])">{{ year['year'] }}<span
                                            style="color: grey; font-size: small">({{ year["num"] }})</span></div>
                                </ElCheckbox>
                            </ElCheckboxGroup>
                        </div>
                    </ElCard>
                </ElCol>
                <ElCol :span="16">
                    <ElRow justify="center" :gutter="20" style="margin: calc(min(4%, 45px)); height: calc(max(4vh, 45px));">
                        <ElCol :span="18" style="height: 100%;">
                            <ElInput id="ei" v-model="content" style="height: 100%; font-size: large;"
                                @keydown.enter=search>
                                <template #suffix style="width: 20px;">
                                    <ElSelect style="width: 100%; margin-left: auto;" v-model="searchOptionVal">
                                        <ElOptionGroup v-if="enableAll">
                                            <ElOption label="All" value="All" />
                                        </ElOptionGroup>
                                        <ElOptionGroup>
                                            <ElOption v-for="item in SearchOption" :label="item.value"
                                                :value="item.value" />
                                        </ElOptionGroup>
                                    </ElSelect>
                                </template>
                            </ElInput>
                        </ElCol>
                        <ElCol :span="5" style="flex: auto; max-width:fit-content;">
                            <ElButton class="search-btn-res" style="height: 100%;" @click="search"> 搜索 <ElIcon>
                                    <Search />
                                </ElIcon>
                            </ElButton>
                        </ElCol>
                    </ElRow>
                    <div v-if="!emptyResult"
                        style="font-family:sans-serif; color: gray; margin-right: 10px; margin-bottom: 20px; margin-left: 20px;">
                        Search done.
                        Found
                        {{ result_total_num
                        }} {{ (result_total_num === 1 ? "result" : "results") }}. </div>
                    <div v-if="emptyResult" class="nores"> Sorry! Found no result </div>
                    <ElCard shadow="hover" v-for="data in datalist"
                        style="margin: 20px 20px 20px 20px; padding: 10px 10px 10px 10px;">
                        <!-- v-show="filterYearCheckList.includes(data['_source']['year'])"> -->
                        <div style="margin: 0px 5px 20px 5px;" class="title"> {{ data['_source']["title"] }} </div>
                        <div style="margin: 10px 5px 10px 5px; align-items: center;">
                            <span style="margin-left: 5px; margin-right: 5px;">
                                <el-icon>
                                    <Calendar />
                                </el-icon>
                                {{ data['_source']["year"] }}
                            </span>
                        </div>
                        <div style="margin: 10px 5px 10px 5px; align-items: center;">
                            <span style="margin-left: 5px; margin-right: 5px; font-size: smaller;">
                                <el-icon>
                                    <User />
                                </el-icon>
                                {{ convertList(data['_source']['authors']) }}
                            </span>
                        </div>
                        <div v-if="data['_source']['keywords'].length !== 0"
                            style="margin: 10px 5px 10px 5px; align-items: center;">
                            <span style="margin-left: 5px; margin-right: 5px; font-size: smaller;">
                                <el-icon>
                                    <Star />
                                </el-icon>
                                {{ convertList(data['_source']['keywords']) }}
                            </span>
                        </div>
                        <div style="margin: 30px 5px 10px 5px;" v-if="data['_source']['link'] && data['link'] !== ''">
                            <ElButton style="default" @click="gotoLink(data['_source']['link'])"> link </ElButton>
                        </div>
                    </ElCard>
                    <el-pagination layout="prev, pager, next" :total="result_total_num" hide-on-single-page="true"
                        :page-size="size_per_page" v-model:current-page="currentPage" />
                </ElCol>
                <ElCol :span="5">
                    <ElCard style="margin-top: 20px;" class="preset1">
                        <div style="height: 200px;">
                            <chart ref="chartYear" :data="childData"></chart>
                        </div>
                    </ElCard>
                </ElCol>
            </ElRow>
        </ElMain>
        <ElFooter class="res">
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
