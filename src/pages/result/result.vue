<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElMenu, ElMenuItem, ElRow, ElCol, ElFooter, ElText, ElCheckboxGroup } from 'element-plus';
import { ElMessage } from 'element-plus';
import { onMounted, reactive, ref, watch, onBeforeMount, toRaw, nextTick } from 'vue'
import { Search, Calendar, User, Star, Select, CloseBold, Filter, Document, Reading } from '@element-plus/icons-vue'
import { useCookies } from 'vue3-cookies'
import LOGO_S from "@/assets/LOGO_S_LONG.png"
import LOGO_L from "@/assets/LOGO_DARK.png"
import API from '../../components/axios_instance'
import chart from '../../components/echarts/chart.vue'
import no_res_logo from '@/assets/no-result.png'
import server_error_logo from '@/assets/server_error.png'
import love_empty from '@/assets/love_empty.png'
import love_fill from '@/assets/love_fill.png'

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
const { cookies } = useCookies()
const isSignIn = ref(false)
const username = ref("")
const showDetail = ref(false)
const likedPaperId = ref({})

function getQueryContent(name) {
    let reg = new RegExp(name + '=([^&]*)')
    let r = window.location.href.match(reg)
    if (r != null) {
        return decodeURIComponent(r[1])
    }
}

const content = ref(getQueryContent('content'))
const enableAll = ref(false)
let carddata = ref()

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

function gotoAuthor(author) {
    searchOptionVal.value = 'Author'
    content.value = author
    search()
}

function gotoKeyword(keyword) {
    searchOptionVal.value = 'Keywords'
    content.value = keyword
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

function fetchPDF(paperid) {
    if (!isSignIn.value) {
        signin()
        return
    }
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    API({
        url: base + `/file/${paperid}`,
        method: 'get'
    }).then((e) => {
        const file_dir = process.env.NODE_ENV === "development" ? "/api/api_port/file" : "/paper_files"
        window.open(file_dir + e['data'], "_blank")
    }).catch(() => {
        ElMessage("Oops! Internal server error. Try again later.")
    })
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

function addLikedList(id) {
    if (!isSignIn.value) {
        signin()
        return
    }
    if (id in likedPaperId.value) {
        delete likedPaperId.value[id]
    } else {
        likedPaperId.value[id] = true
    }
    localStorage.setItem("M_sc_liked", JSON.stringify(likedPaperId.value))
}

onBeforeMount(() => {
    get()
})

onMounted(() => {
    chartYear.value.init()
    isSignIn.value = checkLoginStatus()
    likedPaperId.value = JSON.parse(localStorage.getItem("M_sc_liked"))
})

function gotoProfile() {
    window.open("./profile.html", "_self")
}

function checkLoginStatus() {
    if (cookies.get('M_sc_login_flag') !== null) {
        username.value = localStorage.getItem("M_sc_username")
        return true
    } else {
        return false
    }
}

function signin() {
    window.open("./login.html", "_self")
}

function signup() {
    window.open("./signup.html", "_self")
}

function openDetail(data) {
    console.log(data)
    carddata = data
    showDetail.value = true
}
</script>

<template>
    <Transition>
        <div v-if="showDetail"
            style="z-index: 5;position: fixed; display: flex; width: 100vw; height: 100vh; justify-content: center; align-items: center;">
            <div @click="showDetail = false" style="position: absolute; width: 100%; height: 100%; filter: opacity(0.7)"
                class="detailbg">
            </div>
            <div style="display: flex; width: 85%; z-index: 2; align-items: center;">
                <ElCard style="width: 100%; max-height: 90vh; overflow: auto;" class="detail">
                    <template #header>
                        <div class="title"
                            style="margin-left: 20px; margin-top: 20px; margin-right: 20px; display: flex; flex-direction: row;">
                            <ElButton size="large" class="close" @click="showDetail = false">
                                <el-icon size="large">
                                    <CloseBold />
                                </el-icon>
                            </ElButton>
                            <div style="margin-left: 20px; font-size: 30px;">
                                <span class="title" @click="gotoOrigin(carddata['_source']['link'])">{{
                                    carddata['_source']["title"]
                                }}
                                </span>
                            </div>
                        </div>
                    </template>

                    <div style="margin-left: 20px; margin-top: 10px; align-items: center; display: flex;">
                        <span style="margin-left: 5px; margin-right: 5px;">
                            <span class="inflogo">
                                Year
                            </span>
                            <span class="year links" style="margin-left: 6px; font-size: medium;"
                                @click="gotoYear(carddata['_source']['year'])">
                                {{ carddata['_source']["year"] }}
                            </span>
                        </span>
                    </div>
                    <div style="margin-left: 20px; margin-top: 20px; align-items: center; display: flex;">
                        <span style="margin-left: 5px; margin-right: 5px;">
                            <span class="inflogo">
                                DOI
                            </span>
                            {{ carddata['_source']['doi'] }}
                        </span>
                    </div>
                    <div style="margin-left: 20px; margin-top: 20px; align-items: center; display: flex;">
                        <span style="margin-left: 5px; margin-right: 5px;">
                            <span class="inflogo">
                                Jurnal
                            </span>
                            {{ carddata['_source']['journal'] }}
                        </span>
                    </div>
                    <div style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center;">
                        <span
                            style="margin-left: 5px; margin-right: 5px; font-size: medium; display: flex; align-items: center;">
                            <span class="inflogo">
                                Authors
                            </span>
                            <span style="margin-left: 5px; margin-right: 5px; font-size: medium;">
                                <span v-for="author in carddata['_source']['authors']"
                                    style="margin-right: 12px;line-height: 1.3em;" class="links"
                                    @click="gotoAuthor(author)">
                                    {{ author }}
                                </span>
                            </span>
                        </span>
                    </div>
                    <div v-if="carddata['_source']['keywords'].length !== 0"
                        style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center;">
                        <span
                            style="margin-left: 5px; margin-right: 5px; font-size: medium; display: flex; align-items: center;">
                            <span class="inflogo">
                                Keywords
                            </span>
                            <span style="margin-left: 5px; margin-right: 5px; font-size: medium;">
                                <span v-for="keyword in carddata['_source']['keywords']"
                                    style="margin-right: 15px; line-height: 1.3em;" class="links"
                                    @click="gotoKeyword(keyword)">
                                    {{ keyword }}
                                </span>
                            </span>
                        </span>
                    </div>
                    <div v-if="carddata['_source']['abstract'] !== 0"
                        style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center;">
                        <span style="margin-left: 5px; margin-right: 5px; font-size: medium; display: flex;">
                            <span class="inflogo">
                                Abstract
                            </span>
                            <span
                                style="margin-left: 5px; margin-right: 5px; font-size: 14px; line-height: 1.5em; padding-left: 5px; padding-right: 5px;">
                                {{ carddata['_source']['abstract'] }}
                            </span>
                        </span>
                    </div>
                    <div style="margin: 40px 20px 10px 20px;" v-if="carddata['_source']['link'] && carddata['link'] !== ''">
                        <ElButton class="icon" @click="fetchPDF(carddata['_source']['paper_id'])">
                            <el-icon>
                                <Document />
                            </el-icon>
                            <span>origin pdf</span>
                        </ElButton>
                        <ElButton class="icon" @click="addLikedList(carddata['_source']['paper_id'])">
                            <ElImage :src="love_empty" fit="contain" style="width: 18px; margin: 0;"
                                v-if="!(carddata['_source']['paper_id'] in likedPaperId)" />
                            <ElImage :src="love_fill" fit="contain" style="width: 18px; margin: 0;"
                                v-if="carddata['_source']['paper_id'] in likedPaperId" />
                            <span style="margin-left: 5px;">like</span>
                        </ElButton>
                    </div>
                </ElCard>
            </div>
        </div>
    </Transition>

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
                    <ElCol :span="16" style="height: 38px; display: flex;">
                        <ElInput id="ei" v-model="content" style="height: 100%; font-size: large;" @keydown.enter=search>
                            <template #append>
                                <ElButton class="search-btn-res" style="height: 100%;" @click="search">
                                    <ElIcon style="height: 100%;">
                                        <Search />
                                    </ElIcon>
                                </ElButton>
                            </template>
                        </ElInput>

                        <ElDivider direction="vertical"
                            style="height: 95%; display: flex; margin-top: auto; margin-left: 20px; margin-right: 20px;" />

                        <div v-if="!isSignIn" style="display: flex; margin:auto;;">
                            <ElButton @click="signup" class="resultpage-signin-btn hasborder">sign up</ElButton>
                            <ElButton @click="signin" class="resultpage-signin-btn">sign in</ElButton>
                        </div>
                        <div v-if="isSignIn" style="display: flex; margin:auto;">
                            <ElAvatar @click="gotoProfile">{{ username }} </ElAvatar>
                        </div>
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
                            <ElSlider style="margin-top: 15px; margin-left: 20px; margin-right: 20px; width: auto;"
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
                            <div class="title">
                                <span class="title" @click="openDetail(data)">{{ data['_source']["title"]
                                }}</span>
                            </div>
                        </template>
                        <div style="margin: 10px 5px 10px 5px; align-items: center; display: flex;">
                            <ElTooltip effect="customized" content="Year" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 5px;">
                                    <el-icon>
                                        <Calendar />
                                    </el-icon>
                                    <span class="year links" style="margin-left: 8px;"
                                        @click="gotoYear(data['_source']['year'])">
                                        {{ data['_source']["year"] }}
                                    </span>
                                </span>
                            </ElTooltip>
                            <span style="margin-left: 20px; margin-right: 5px; font-size: smaller;">
                                <span class="inflogo">
                                    DOI
                                </span>
                                {{ data['_source']['doi'] }}
                            </span>
                            <ElTooltip effect="customized" content="Journal" placement="right" show-after="800">
                                <span style="margin-left: 20px; margin-right: 5px; font-size: smaller;">
                                    <el-icon>
                                        <Reading />
                                    </el-icon>
                                    <span style="margin-left: 8px;">
                                        {{ data['_source']['journal'] }}
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
                                    <span v-for="author in data['_source']['authors']" style="margin-left: 12px;"
                                        class="links" @click="gotoAuthor(author)">
                                        {{ author }}
                                    </span>
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
                                    <span v-for="keyword in data['_source']['keywords']" style="margin-left: 12px;"
                                        class="links" @click="gotoKeyword(keyword)">
                                        {{ keyword }}
                                    </span>
                                </span>
                            </ElTooltip>
                        </div>
                        <div style="margin: 20px 5px 10px 5px;">
                            <ElButton v-if="data['_source']['link'] && data['link'] !== ''" class="icon"
                                @click="fetchPDF(data['_source']['paper_id'])">
                                <el-icon>
                                    <Document />
                                </el-icon>
                                <span>origin pdf</span>
                            </ElButton>
                            <ElButton class="icon" @click="addLikedList(data['_source']['paper_id'])">
                                <ElImage :src="love_empty" fit="contain" style="width: 18px; margin: 0;"
                                    v-if="!(data['_source']['paper_id'] in likedPaperId)" />
                                <ElImage :src="love_fill" fit="contain" style="width: 18px; margin: 0;"
                                    v-if="data['_source']['paper_id'] in likedPaperId" />
                                <span style="margin-left: 5px;">like</span>
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
