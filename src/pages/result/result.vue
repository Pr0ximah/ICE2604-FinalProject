<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElMenu, ElMenuItem, ElRow, ElCol, ElFooter, ElText, ElCheckboxGroup } from 'element-plus';
import { ElMessage } from 'element-plus';
import { onMounted, reactive, ref, watch, onBeforeMount, toRaw, nextTick } from 'vue'
import { Search, Calendar, User, Star, Select, CloseBold, Filter, Document } from '@element-plus/icons-vue'
import LOGO_S from "@/assets/LOGO_S_LONG.png"
import LOGO_L from "@/assets/LOGO_DARK.png"
import API from '../../components/axios_instance'
import chart from '../../components/echarts/chart.vue'
import no_res_logo from '@/assets/no-result.png'
import server_error_logo from '@/assets/server_error.png'

let chartYear = ref()
let datalist = ref()
let datalistAllFiltered = ref()
let datalistAll = ref()
let childData = ref()
let filterButtonStatus = ref(true)
let result_total_num = ref(0)
const size_per_page = ref(15)   // 每页显示的条目数
let emptyResult = ref(true)
let searchOptionVal = ref("")
let currentPage = ref(1)
let filterYearList = ref()
const server_error = ref(false)
const filterYearChecked = ref([])
const filterYearRange = ref([0, 0])
const filterYearRangeMax = ref(0)
const filterYearRangeMin = ref(0)
let filterYearRangeShow = ref(false)
let showLoadingSkeleton = ref(false)

function getQueryContent(name) {
    let reg = new RegExp(name + '=([^&]*)')
    let r = window.location.href.match(reg)
    if (r != null) {
        return decodeURIComponent(r[1])
    }
}

const content = ref(getQueryContent('content'))
const enableAll = ref(false)

function get() {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const content = encodeURIComponent(getQueryContent('content'))
    const type = encodeURIComponent(getQueryContent('type'))
    showLoadingSkeleton.value = true;
    API({
        url: base + `/search/content=${content}&type=${type}`,
        method: 'get'
    }).then((e) => {
        server_error.value = false;
        datalistAll.value = e['data']['data']
        filterYearList.value = e['data']['year_list']
        result_total_num = datalistAll.value.length
        datalistAllFiltered.value = datalistAll.value
        filterButtonStatus.value = true
        selectAllYear()
        if (datalistAll.value.length !== 0) {
            filterYearRangeMax.value = filterYearList['_rawValue'][filterYearList.value.length - 1]['year']
            filterYearRangeMin.value = filterYearList['_rawValue'][0]['year']
            filterYearRange.value[0] = filterYearRangeMin.value
            filterYearRange.value[1] = filterYearRangeMax.value
            if (filterYearRangeMin.value === filterYearRangeMax.value) {
                filterYearRangeShow.value = false;
            } else {
                filterYearRangeShow.value = true;
            }
        } else {
            filterYearRangeShow.value = false;
        }
        childData.value = datalistAll.value
        emptyResult = (result_total_num == 0)
        const type = getQueryContent('type')
        if (searchOptionVal.value != type) {
            searchOptionVal.value = type
        }
        switchPage()
        showLoadingSkeleton.value = false;
    }).catch(() => {
        server_error.value = true;
        const type = getQueryContent('type')
        if (searchOptionVal.value != type) {
            searchOptionVal.value = type
        }
        showLoadingSkeleton.value = false;
    }).then(() => {
        chartYear.value.init()
    })
}

function selectAllYear() {
    for (let i = 0; i < filterYearList.value.length; i++) {
        filterYearChecked.value.push(filterYearList.value[i]['year'])
    }
    refreshFilterYear()
}

function refreshFilterYearRange() {
    let filterYearCheckedNew = []
    for (let i = 0; i < filterYearList.value.length; i++) {
        let year = filterYearList['_rawValue'][i]['year']
        if (year >= filterYearRange['_rawValue'][0] && year <= filterYearRange['_rawValue'][1]) {
            filterYearCheckedNew.push(year)
        }
    }
    filterYearChecked.value = filterYearCheckedNew
}

function gotoYear(year) {
    searchOptionVal.value = 'Year'
    content.value = year
    search()
}

function selectNoneYear() {
    filterYearChecked.value = []
    refreshFilterYear()
}

function refreshFilterYear() {
    datalistAllFiltered.value = []
    for (let i = 0; i < datalistAll.value.length; i++) {
        if (toRaw(filterYearChecked)['_rawValue'].includes(toRaw(datalistAll)['_rawValue'][i]['_source']['year'])) {
            datalistAllFiltered.value.push(datalistAll.value[i])
        }
    }
    result_total_num = datalistAllFiltered.value.length
    childData.value = datalistAllFiltered.value
    currentPage.value = 1
    switchPage()
    nextTick()
}

function switchPage() {
    let start = (currentPage.value - 1) * size_per_page.value
    let end = currentPage.value * size_per_page.value
    if (end >= result_total_num) {
        end = result_total_num
    }
    datalist.value = datalistAllFiltered.value.slice(start, end)
}

watch(filterYearChecked, () => {
    refreshFilterYear()
})

window.onresize = () => {
    setTimeout(() => {
        chartYear.value.resizeChart()
    }, 200)
}

watch(currentPage, () => {
    switchPage()
    window.scrollTo({
        top: 0
    })
})

watch(filterYearRange, () => {
    refreshFilterYearRange()
})

function switchFilterStatus() {
    filterButtonStatus.value = !filterButtonStatus.value
    if (filterButtonStatus.value) {
        selectAllYear()
    } else {
        selectNoneYear()
    }
}

function fetchPDF(url) {
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
    ElMessage("The input is empty.")
    return
  } else {
    if (searchOptionVal.value === "Year" && !/^[0-9]*$/.test(content.value)) {
      ElMessage("Year can only be an integer.")
      return
    }
    gotoResult()
  }
}

function gotoResult() {
    let inputVal = encodeURIComponent(content.value)
    let optionVal = encodeURIComponent(searchOptionVal.value)
    window.open(`./search.html?content=${inputVal}&type=${optionVal}`, "_self")
}

function gotoOrigin(url) {
    if (url !== undefined) {
        window.open(url, "_blank")
    } else {
        ElMessage("暂无原文链接")
    }
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
            <ElMenu mode="horizontal" :ellipsis="false" style="width: 100%;" ref="menu">
                <ElMenuItem :index="0" @click="backToHome">
                    <ElImage class="left-menu-logo" :src="LOGO_S" fit="contain" />
                </ElMenuItem>
                <ElRow :gutter="10"
                    style="min-width: 700px; height: 96%; align-self: right; display: flex; justify-content: right; width: 50%; margin: auto; margin-right: 1%;">
                    <ElCol :span="4">
                        <ElSelect class="menuselect" style="width: 100%;" v-model="searchOptionVal">
                            <ElOptionGroup v-if="enableAll">
                                <ElOption label="All" value="All" />
                            </ElOptionGroup>
                            <ElOptionGroup>
                                <ElOption v-for="item in SearchOption" :label="item.value" :value="item.value" />
                            </ElOptionGroup>
                        </ElSelect>
                    </ElCol>
                    <ElCol :span="13" style="height: 38px;">
                        <ElInput id="ei" v-model="content" style="height: 100%; font-size: large;" @keydown.enter=search>
                            <template #append>
                                <ElButton class="search-btn-res" style="height: 100%;" @click="search">
                                    <ElIcon style="height: 100%;">
                                        <Search />
                                    </ElIcon>
                                </ElButton>
                            </template>
                        </ElInput>
                    </ElCol>
                </ElRow>
            </ElMenu>
        </ElHeader>
        <ElMain class="result">
            <ElRow style="width: 100%; margin: auto;" :gutter="5" justify="center">
                <ElCol :span="3" style="height: 100%">
                    <ElCard class="preset1" style="margin-top: 20px; width: 100%;">
                        <div style="text-align: center;">
                            <ElText style="font-size: 22px; letter-spacing: 0.03em;">filter</ElText>
                            <el-icon style="margin-left: 2%;">
                                <Filter />
                            </el-icon>
                        </div>
                        <ElDivider border-style="dashed" style="margin-top: 15px; margin-bottom: 15px;"></ElDivider>
                        <div>
                            <div style="margin-bottom: 10px; text-align: center;">
                                <ElText style="font-size: medium; color: gray">Year</ElText>
                                <ElButton @click="switchFilterStatus" class="icon" style="margin-left: 5px;" size="small"
                                    circle="true" :disabled="emptyResult">
                                    <el-icon v-if="!filterButtonStatus"><Select /></el-icon>
                                    <el-icon v-if="filterButtonStatus">
                                        <CloseBold />
                                    </el-icon>
                                </ElButton>
                            </div>
                            <ElCheckboxGroup v-model="filterYearChecked" style="justify-items: center; text-align: center;">
                                <ElCheckbox v-for="year in filterYearList" :label="year['year']"
                                    style="margin:1px 6% 1px 6%;">
                                    <div style="font-size: small; margin: auto;">{{ year['year'] }} <span
                                            style="color: grey; font-size: small">({{ year["num"] }}) </span></div>
                                </ElCheckbox>
                            </ElCheckboxGroup>
                            <ElSlider style="margin-top: 15px; margin-left: 5px; margin-right: 5px; width: auto;"
                                v-model="filterYearRange" range :max="filterYearRangeMax" :min="filterYearRangeMin"
                                v-if="filterYearRangeShow" />
                        </div>
                    </ElCard>
                </ElCol>
                <ElCol :span="16">
                    <div v-if="emptyResult && !server_error" class="nores" style="margin-top: 5%;"
                        v-show="!showLoadingSkeleton">
                        <div>Sorry! Found no result</div>
                        <ElImage :src="no_res_logo" fit="contain" style="margin: 50px;" />
                    </div>
                    <div v-if="server_error" class="server_error" style="margin-top: 5%;" v-show="!showLoadingSkeleton">
                        <div>Oops! Something went wrong with server, please try again later.</div>
                        <ElImage :src="server_error_logo" fit="contain" style="margin: 50px;" />
                    </div>
                    <ElCard shadow="hover" v-for="data in datalist"
                        style="margin: 20px 20px 20px 20px; padding: 10px 10px 10px 10px;" v-show="!showLoadingSkeleton">
                        <template #header>
                            <!-- <div style="margin: 0px 5px 20px 5px;" class="title"> -->
                            <div class="title">
                                <span class="title" @click="gotoOrigin(data['_source']['link'])">{{ data['_source']["title"]
                                }}</span>
                            </div>
                        </template>
                        <div style="margin: 10px 5px 10px 5px; align-items: center;">
                            <ElTooltip effect="customized" content="Year" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 5px;">
                                    <el-icon>
                                        <Calendar />
                                    </el-icon>
                                    <!-- <span class="year" style="margin-left: 4px;" @click="gotoYear(data['_source']['year'])"> -->
                                    <span class="year" style="margin-left: 6px;">
                                        {{ data['_source']["year"] }}
                                    </span>
                                </span>
                            </ElTooltip>
                        </div>
                        <div style="margin: 10px 5px 10px 5px; align-items: center;">
                            <ElTooltip effect="customized" content="Authors" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 5px; font-size: smaller;">
                                    <el-icon>
                                        <User />
                                    </el-icon>
                                    {{ convertList(data['_source']['authors']) }}
                                </span>
                            </ElTooltip>
                        </div>
                        <div v-if="data['_source']['keywords'].length !== 0"
                            style="margin: 10px 5px 10px 5px; align-items: center;">
                            <ElTooltip effect="customized" content="Keywords" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 5px; font-size: smaller;">
                                    <el-icon>
                                        <Star />
                                    </el-icon>
                                    {{ convertList(data['_source']['keywords']) }}
                                </span>
                            </ElTooltip>
                        </div>
                        <div style="margin: 20px 5px 10px 5px;" v-if="data['_source']['link'] && data['link'] !== ''">
                            <ElButton class="icon" @click="fetchPDF(data['_source']['link'])">
                                <el-icon>
                                    <Document />
                                </el-icon>
                                <span>origin pdf</span>
                            </ElButton>
                        </div>
                    </ElCard>
                    <el-pagination layout="prev, pager, next" :total="result_total_num" hide-on-single-page="true"
                        :page-size="size_per_page" v-model:current-page="currentPage" v-show="!showLoadingSkeleton" />
                    <div v-if="!emptyResult" style="font-family:sans-serif; color: gray;" v-show="!showLoadingSkeleton"
                        class="searchres">
                        Search done. Found {{ result_total_num }} {{ (result_total_num === 1 ? "result" : "results") }}.
                    </div>
                    <el-skeleton :rows="10" animated v-show="showLoadingSkeleton"
                        style="margin: auto; margin-top: 5%; width: 80%; justify-self: center;" throttle="500" />
                </ElCol>
                <ElCol :span="5">
                    <ElCard style="margin-top: 20px; height: 25vh;" class="preset1" id="chart">
                        <div style="height: 100%;">
                            <chart ref="chartYear" :data="childData"></chart>
                        </div>
                    </ElCard>
                </ElCol>
            </ElRow>
        </ElMain>
        <ElFooter class="res">
            <ElImage class="bottom-logo" :src="LOGO_L" fit="contain"
                style="height: 70%; margin: 20px 0px 25px 0px; margin-left: 1%; width: auto;" />
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
