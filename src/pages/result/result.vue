<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElMenu, ElMenuItem, ElRow, ElCol, ElFooter, ElText, ElCheckboxGroup } from 'element-plus';
import { ElMessage, ElLoading } from 'element-plus';
import { onMounted, reactive, ref, watch, onBeforeMount, toRaw, nextTick } from 'vue'
import { Search, Calendar, User, Star, Select, CloseBold, Filter, Document, Reading } from '@element-plus/icons-vue'
import { useCookies } from 'vue3-cookies'
import LOGO_S from "@/assets/LOGO_S_LONG.png"
import LOGO_L from "@/assets/LOGO_DARK.png"
import API from '../../components/axios_instance'
import chartYearOri from '../../components/echarts/chartYearOri.vue'
import chartAuthorOri from '../../components/echarts/chartAuthorOri.vue'
import no_res_logo from '@/assets/no-result.png'
import server_error_logo from '@/assets/server_error.png'
import love_empty from '@/assets/love_empty.png'
import love_fill from '@/assets/love_fill.png'
import author_graph_bg from '@/assets/author_graph_bg.png'
import { verifyLoginStatus } from '../../components/account_func'

let chartYear = ref()
let chartAuthor = ref()
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
let show_author_name_on_graph = ref(false)
const showAuthorGraph = ref(false)

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

function getSearchDataList() {
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
        emptyResult.value = (result_total_num == 0)
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
        if (chartYear) {
            chartYear.value.resizeChart()
        }
        if (chartAuthor) {
            chartAuthor.value.resizeChart()
        }
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
        deleteLikedPaper2BE(username.value, id)
    } else {
        addLikedPaper2BE(username.value, id)
    }
}

function addLikedPaper2BE(username, id) {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username)
    const paper_id = encodeURIComponent(id)
    likedPaperId.value[id] = true
    API({
        url: base + `/collectpaper`,
        method: 'post',
        data: {
            user: usrname,
            paper_id: paper_id,
        }
    }).catch(() => {
        delete likedPaperId.value[id]
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

function deleteLikedPaper2BE(username, id) {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username)
    const paper_id = encodeURIComponent(id)
    delete likedPaperId.value[id]
    API({
        url: base + `/removepaper`,
        method: 'post',
        data: {
            user: usrname,
            paper_id: paper_id,
        }
    }).catch(() => {
        likedPaperId.value[id] = true
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

onBeforeMount(() => {
    getSearchDataList()
})

onMounted(() => {
    chartYear.value.init()
    checkLoginStatus()
    refreshLikedList()
})

function refreshLikedList() {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username.value)
    API({
        url: base + `/get_collected_paper`,
        method: 'post',
        data: {
            user: usrname,
        }
    }).then((e) => {
        for (let i in e.data) {
            likedPaperId.value[i] = true
        }
    }).catch((e) => {
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

function gotoProfile() {
    localStorage.setItem("M_sc_lastpage", window.location.href)
    window.open("./profile.html", "_self")
}

async function checkLoginStatus() {
    if (cookies.get('M_sc_login_flag')) {
        username.value = localStorage.getItem("M_sc_username")
        let key = cookies.get("M_sc_login_key")
        verifyLoginStatus(username.value, key).then(e => {
            if (!e.data) {
                ElMessage("Your login status has been expired, please login again!")
                isSignIn.value = false
                setTimeout(() => {
                    cookies.remove("M_sc_login_flag")
                }, 2000);
            } else {
              isSignIn.value = true
            }
        })
    } else {
        isSignIn.value = false
    }
}

function signin() {
    localStorage.setItem("M_sc_lastpage", window.location.href)
    window.open("./login.html", "_self")
}

function signup() {
    localStorage.setItem("M_sc_lastpage", window.location.href)
    window.open("./signup.html", "_self")
}

function openDetail(data) {
    carddata = data
    showDetail.value = true
}

function openAuthorGraph() {
    showAuthorGraph.value = true
    let authorname = null
    let temp = datalistAllFiltered.value[0]['_source']['authors']
    for (let i in temp) {
        if (temp[i].toLowerCase().includes(content.value.toLowerCase())) {
            authorname = temp[i]
            break
        }
    }
    if (!authorname) {
        ElMessage("Author name is not correct, no data.")
        return
    }
    setTimeout(() => {
        chartAuthor.value.init(datalistAllFiltered.value, authorname)
    }, 200)
}
</script>

<template>
    <Transition>
        <div v-if="showAuthorGraph"
            style="z-index: 5;position: fixed; display: flex; width: 100vw; height: 100vh; justify-content: center; align-items: center;">
            <div @click="showAuthorGraph = false"
                style="position: absolute; width: 100%; height: 100%; filter: opacity(0.7)" class="detailbg">
            </div>
            <div style="display: flex; width: 85%; height: 80%; z-index: 2; align-items: center;">
                <ElCard style="width: 100%; height: 100%; overflow: auto;" class="author_graph_card">
                    <template #header>
                        <div class="title"
                            style="margin-left: 20px; margin-top: 10px; margin-right: 20px; display: flex; flex-direction: row;">
                            <ElButton size="large" class="close" @click="showAuthorGraph = false">
                                <el-icon size="large">
                                    <CloseBold />
                                </el-icon>
                            </ElButton>
                            <div style="margin-left: 20px; font-size: xx-large; font-family: 'Helvetica'; font-weight: 550;">
                                Author Force Graph
                            </div>
                        </div>
                    </template>
                    <chart-author-ori style="" ref="chartAuthor"></chart-author-ori>
                </ElCard>
            </div>
        </div>
    </Transition>

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
                                <span class="title" @click.stop="gotoOrigin(carddata['_source']['link'])">{{
                                    carddata['_source']["title"]
                                }}
                                </span>
                            </div>
                        </div>
                    </template>

                    <div style="margin-left: 20px; margin-top: 10px; align-items: center; display: flex;">
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
                                Year
                            </span>
                            <span class="year links" style="margin-left: 6px;"
                                @click.stop="gotoYear(carddata['_source']['year'])">
                                {{ carddata['_source']["year"] }}
                            </span>
                        </span>
                    </div>
                    <div style="margin-left: 20px; margin-top: 20px; align-items: center; display: flex;">
                        <span style="margin-left: 5px; margin-right: 5px;">
                            <span class="inflogo">
                                Journal
                            </span>
                            <span style="line-height: 1.6em;">
                                {{ carddata['_source']['journal'] }}
                            </span>
                        </span>
                    </div>
                    <div style="margin-left: 20px; margin-top: 20px; align-items: center; display: flex;">
                        <span style="margin-left: 5px; margin-right: 5px;">
                            <span class="inflogo">
                                Authors
                            </span>
                            <span style="margin-left: 5px; margin-right: 5px; line-height: 1.6em;">
                                <span v-for="author in carddata['_source']['authors']" style="margin-right: 12px;"
                                    class="links" @click.stop="gotoAuthor(author)">
                                    {{ author }}
                                </span>
                            </span>
                        </span>
                    </div>
                    <div v-if="carddata['_source']['keywords'] && carddata['_source']['keywords'].length !== 0"
                        style="margin-left: 20px; margin-top: 20px; align-items: center; display: flex;">
                        <span style="margin-left: 5px; margin-right: 5px;">
                            <span class="inflogo">
                                Keywords
                            </span>
                            <span style="margin-left: 5px; margin-right: 5px; line-height: 1.6em;">
                                <span v-for="keyword in carddata['_source']['keywords']"
                                    style="margin-right: 12px; word-break: break-word;" class="links"
                                    @click.stop="gotoKeyword(keyword)">
                                    {{ keyword }}
                                </span>
                            </span>
                        </span>
                    </div>
                    <div v-if="carddata['_source']['abstract'] && carddata['_source']['abstract'] !== 0"
                        style="margin-left: 20px; margin-top: 20px; margin-right: 20px; align-items: center;">
                        <span style="margin-left: 5px; margin-right: 5px; display: flex;">
                            <span class="inflogo">
                                Abstract
                            </span>
                            <span
                                style="margin-left: 5px; margin-right: 5px; font-size: 14px; line-height: 1.5em; padding-left: 5px; padding-right: 5px;">
                                {{ carddata['_source']['abstract'] }}
                            </span>
                        </span>
                    </div>
                    <div style="margin: 40px 20px 10px 20px;" v-if="carddata['_source']['paper_id'] && carddata['paper_id'] !== ''">
                        <ElButton class="icon" @click.stop="fetchPDF(carddata['_source']['paper_id'])">
                            <el-icon>
                                <Document />
                            </el-icon>
                            <span>origin pdf</span>
                        </ElButton>
                        <ElButton class="icon" @click.stop="addLikedList(carddata['_source']['paper_id'])">
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

    <ElContainer class="bg-all" style="height: 100%;">
        <ElHeader>
            <ElMenu mode="horizontal" :ellipsis="false" style="width: 100%;">
                <ElMenuItem :index="0" @click="backToHome">
                    <ElImage class="left-menu-logo" :src="LOGO_S" fit="contain" />
                </ElMenuItem>
                <div
                    style="height: 100%; align-self: center; display: flex; justify-content: right; width: 50%; margin: auto; margin-right: 1%; column-gap: 20px;">
                    <div style="align-self: center; max-width: 120px; min-width: 120px;">
                        <ElSelect class="menuselect" style="width: 100%;" v-model="searchOptionVal">
                            <ElOptionGroup v-if="enableAll">
                                <ElOption label="All" value="All" />
                            </ElOptionGroup>
                            <ElOptionGroup>
                                <ElOption v-for="item in SearchOption" :label="item.value" :value="item.value" />
                            </ElOptionGroup>
                        </ElSelect>
                    </div>
                    <div style="align-self: center; display: flex; flex-direction: row;">
                        <ElInput id="ei" v-model="content" style="height: 100%; min-width: 120px; font-size: large;"
                            @keydown.enter=search>
                            <template #append>
                                <ElButton class="search-btn-res" style="height: 100%;" @click="search">
                                    <ElIcon style="height: 100%;">
                                        <Search />
                                    </ElIcon>
                                </ElButton>
                            </template>
                        </ElInput>

                        <ElDivider direction="vertical"
                            style="height: 34px; align-self: center; margin-left: 15px; margin-right: 13px;" />

                        <div v-if="!isSignIn" style="display: flex; margin:auto;">
                            <ElButton @click="signup" class="resultpage-signin-btn hasborder">sign up</ElButton>
                            <ElButton @click="signin" class="resultpage-signin-btn">sign in</ElButton>
                        </div>
                        <div v-if="isSignIn" style="display: flex; margin:auto;">
                            <ElAvatar @click="gotoProfile" style="font-size: large;">{{ username[0] }} </ElAvatar>
                        </div>
                    </div>
                </div>
            </ElMenu>
        </ElHeader>
        <ElMain class="result">
            <div
                style="display: flex; margin: auto; justify-content: center; margin-left: 20px; margin-right: 20px; margin-top: 5px;">
                <div>
                    <ElCard class="preset1"
                        style="margin-top: 20px; width: 100%; display: flex; align-items: center; justify-content: center;">
                        <div style="text-align: center;">
                            <ElText style="font-size: 22px; letter-spacing: 0.03em;">filter</ElText>
                            <el-icon style="margin-left: 2%;">
                                <Filter />
                            </el-icon>
                        </div>
                        <ElDivider border-style="dashed" style="margin-top: 15px; margin-bottom: 15px;"></ElDivider>
                        <div>
                            <div style="margin-bottom: 10px; text-align: center;">
                                <ElText style="color: gray">Year</ElText>
                                <ElButton @click="switchFilterStatus" class="icon" style="margin-left: 5px;" size="small"
                                    circle="true" :disabled="emptyResult">
                                    <el-icon v-if="!filterButtonStatus"><Select /></el-icon>
                                    <el-icon v-if="filterButtonStatus">
                                        <CloseBold />
                                    </el-icon>
                                </ElButton>
                            </div>
                            <ElCheckboxGroup v-model="filterYearChecked"
                                style="display: flex; flex-direction: column; justify-items: center; text-align: center; margin-left: 30px; margin-right: 30px;">
                                <ElCheckbox v-for="year in filterYearList" :label="year['year']" style="margin: auto;">
                                    <div style="font-size: small; margin: auto;">{{ year['year'] }} <span
                                            style="color: grey; font-size: small">({{ year["num"] }}) </span></div>
                                </ElCheckbox>
                            </ElCheckboxGroup>
                            <ElSlider style="width: 85%; margin: auto; margin-top: 5px;" v-model="filterYearRange" range
                                :max="filterYearRangeMax" :min="filterYearRangeMin" v-if="filterYearRangeShow" />
                        </div>
                    </ElCard>
                </div>
                <div style="width: 70%">
                    <div v-if="emptyResult && !server_error" class="nores" style="margin-top: 5%;"
                        v-show="!showLoadingSkeleton">
                        <div>Sorry! Found no result</div>
                        <ElImage :src="no_res_logo" fit="contain" style="margin: 50px;" />
                    </div>
                    <div v-if="server_error" class="server_error" style="margin-top: 5%;" v-show="!showLoadingSkeleton">
                        <div>Oops! Something went wrong with server, please try again later.</div>
                        <ElImage :src="server_error_logo" fit="contain" style="margin: 50px;" />
                    </div>
                    <ElCard class="data" shadow="hover" v-for="data in datalist"
                        style="margin: 20px 20px 20px 20px; padding: 10px 10px 10px 10px;" @click="openDetail(data)"
                        v-show="!showLoadingSkeleton">
                        <template #header>
                            <div class="title">
                                <span class="title" @click.stop="gotoOrigin(data['_source']['link'])">{{
                                    data['_source']["title"]
                                }}</span>
                            </div>
                        </template>
                        <div
                            style="margin: 10px 5px 10px 5px; align-items: center; display: flex; flex-wrap: wrap; row-gap: 15px;">
                            <span style="margin-left: 5px; margin-right: 15px; font-size: smaller;">
                                <span class="inflogo">
                                    DOI
                                </span>
                                <span style="line-height: 1.6em; word-break: break-word;">
                                    {{ data['_source']['doi'] }}
                                </span>
                            </span>
                            <ElTooltip effect="customized" content="Year" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 15px; font-size: smaller;">
                                    <el-icon size="small">
                                        <Calendar />
                                    </el-icon>
                                    <span class="links" style="margin-left: 5px;"
                                        @click.stop="gotoYear(data['_source']['year'])">
                                        {{ data['_source']["year"] }}
                                    </span>
                                </span>
                            </ElTooltip>
                            <ElTooltip effect="customized" content="Journal" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 15px; font-size: smaller;">
                                    <el-icon>
                                        <Reading />
                                    </el-icon>
                                    <span style="margin-left: 8px; line-height: 1.6em;">
                                        {{ data['_source']['journal'] }}
                                    </span>
                                </span>
                            </ElTooltip>
                        </div>
                        <div style="margin: 15px 5px 10px 5px; align-items: center;">
                            <ElTooltip effect="customized" content="Authors" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 15px; font-size: smaller;">
                                    <el-icon>
                                        <User />
                                    </el-icon>
                                    <span v-for="author in data['_source']['authors']"
                                        style="margin-left: 12px; line-height: 1.6em;" class="links"
                                        @click.stop="gotoAuthor(author)">
                                        {{ author }}
                                    </span>
                                </span>
                            </ElTooltip>
                        </div>
                        <div v-if="data['_source']['keywords'] && data['_source']['keywords'].length !== 0"
                            style="margin: 15px 5px 10px 5px; align-items: center;">
                            <ElTooltip effect="customized" content="Keywords" placement="right" show-after="800">
                                <span style="margin-left: 5px; margin-right: 5px; font-size: smaller;">
                                    <el-icon>
                                        <Star />
                                    </el-icon>
                                    <span v-for="keyword in data['_source']['keywords']"
                                        style="margin-left: 12px; line-height: 1.6em; word-break: break-word;" class="links"
                                        @click.stop="gotoKeyword(keyword)">
                                        {{ keyword }}
                                    </span>
                                </span>
                            </ElTooltip>
                        </div>
                        <div style="margin: 20px 5px 10px 5px; display: flex;">
                            <ElButton v-if="data['_source']['paper_id'] && data['paper_id'] !== ''" class="icon"
                                @click.stop="fetchPDF(data['_source']['paper_id'])">
                                <el-icon>
                                    <Document />
                                </el-icon>
                                <span>origin pdf</span>
                            </ElButton>
                            <ElButton class="icon" @click.stop="addLikedList(data['_source']['paper_id'])">
                                <ElImage :src="love_empty" fit="contain" style="width: 18px; margin: 0;"
                                    v-if="!(data['_source']['paper_id'] in likedPaperId)" />
                                <ElImage :src="love_fill" fit="contain" style="width: 18px; margin: 0;"
                                    v-if="data['_source']['paper_id'] in likedPaperId" />
                                <span style="margin-left: 5px;">like</span>
                            </ElButton>
                        </div>
                        <div style="color: grey; font-size: 13px; margin-top: 20px; margin-left: 5px;">
                            click the card to show the details
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
                </div>
                <div style="display: flex; flex-direction: column; row-gap: 40px; width: 20%">
                    <div style="width: 100%; min-width: 210px; height: 25vh; min-height: 210px;">
                        <ElCard style="margin-top: 20px; height: 100%" class="preset1" id="chart">
                            <div style="height: 100%;">
                                <chart-year-ori ref="chartYear" :data="childData"></chart-year-ori>
                            </div>
                        </ElCard>
                    </div>
                    <div style="width: 100%; min-width: 210px; min-height: 210px;">
                        <div style="height: 0; padding-bottom: 100%; position: relative;">
                            <ElCard
                                style="position: absolute; top:0; left:0; right:0; bottom:0; display: flex; flex-direction: column;"
                                class="preset1" id="chart" v-if="searchOptionVal === 'Author' && !emptyResult">
                                <div
                                    style="height: 5%; font-weight: 600; font-family: 'Helvetica'; font-size: 20px; margin-left: 5px;">
                                    Author Force Graph
                                </div>
                                <div style="position: relative; width: 100%; height: 95%;"
                                    @mouseenter="show_author_name_on_graph = true"
                                    @mouseleave="show_author_name_on_graph = false" class="author_graph"
                                    @click="openAuthorGraph">
                                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
                                        <ElImage style="margin: 50px; width: calc(100% - 100px)" :src="author_graph_bg"
                                            fit="contain" />
                                    </div>
                                    <Transition>
                                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; justify-content: center; align-items: center;"
                                            v-show="show_author_name_on_graph">
                                            <span style="font-weight: 550;">
                                                {{ content }}
                                            </span>
                                        </div>
                                    </Transition>
                                </div>
                            </ElCard>
                        </div>
                    </div>
                </div>
            </div>
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
