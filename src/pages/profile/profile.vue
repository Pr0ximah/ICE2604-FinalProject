<script setup>
import { ElButton, ElCard, ElImage, ElInput, ElText, ElMessage } from 'element-plus'
import { ref, onMounted, watch } from 'vue'
import { Document, Back, CloseBold } from '@element-plus/icons-vue'
import { useCookies } from 'vue3-cookies'
import LOGO from "@/assets/LOGO_DARK.png"
import API from '../../components/axios_instance'
import { signup_inner, backToHome, goBack } from '../../components/account_func'
import { verifyLoginStatus } from '../../components/account_func'
import love_empty from '@/assets/love_empty.png'
import love_fill from '@/assets/love_fill.png'

const bgUrl = '/HOMEPAPERS/HOMEPAPER2.png'
const { cookies } = useCookies()
const username = ref("")
const liked = ref({})
const showDetail = ref(false)
const carddata = ref({ '_source': {} })
const likedPaperId = ref({})
const switchLikeStat = ref(true)

function addLikedList(id) {
    if (switchLikeStat.value) {
        switchLikeStat.value = false
        deleteLikedPaper2BE(username.value, id).then(() => {
            refreshLikedList()
        })
    } else {
        switchLikeStat.value = true
        addLikedPaper2BE(username.value, id).then(() => {
            refreshLikedList()
        })
    }
}

async function addLikedPaper2BE(username, id) {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username)
    const paper_id = encodeURIComponent(id)
    likedPaperId.value[id] = true
    return API({
        url: base + `/collectpaper`,
        method: 'post',
        data: {
            user: usrname,
            paper_id: paper_id,
        }
    }).then((e) => {
        return e
    }).catch(() => {
        delete likedPaperId.value[id]
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

watch(showDetail, () => {
    refreshLikedList()
})

async function deleteLikedPaper2BE(username, id) {
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username)
    const paper_id = encodeURIComponent(id)
    delete likedPaperId.value[id]
    return API({
        url: base + `/removepaper`,
        method: 'post',
        data: {
            user: usrname,
            paper_id: paper_id,
        }
    }).then((e) => {
        return e
    }).catch(() => {
        likedPaperId.value[id] = true
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

async function checkLoginStatus() {
    if (cookies.get('M_sc_login_flag')) {
        username.value = localStorage.getItem("M_sc_username")
        let key = cookies.get("M_sc_login_key")
        verifyLoginStatus(username.value, key).then(e => {
            if (!e.data) {
                ElMessage("Your login status has been expired, please login again!")
                setTimeout(() => {
                    cookies.remove("M_sc_login_flag")
                    localStorage.setItem("M_sc_lastpage", window.location.href)
                    window.open('./login.html', '_self')
                }, 2000);
            }
        })
    } else {
        localStorage.setItem("M_sc_lastpage", window.location.href)
        window.open('./login.html', '_self')
    }
}

onMounted(() => {
    checkLoginStatus()
    refreshLikedList()
    // document.title = username.value + " - M Scholar"
    document.title = username.value + " - Profile M_Scholar"
})

function logout() {
    localStorage.removeItem('M_sc_username')
    cookies.remove('M_sc_login_flag')
    goBack()
}

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
        liked.value = e.data
    }).catch((e) => {
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

function showDetailFunc(id) {
    switchLikeStat.value = true
    carddata.value['_source']['link'] = liked.value[id]['Link']
    carddata.value['_source']['doi'] = liked.value[id]['DOI']
    carddata.value['_source']['year'] = liked.value[id]['Year']
    carddata.value['_source']['journal'] = liked.value[id]['Journal']
    carddata.value['_source']['authors'] = liked.value[id]['Authors']
    carddata.value['_source']['keywords'] = liked.value[id]['Keywords']
    carddata.value['_source']['abstract'] = liked.value[id]['Abstract']
    carddata.value['_source']['paper_id'] = liked.value[id]['ID']
    carddata.value['_source']['title'] = liked.value[id]['Title']
    showDetail.value = true
}

function gotoOrigin(url) {
    if (url !== undefined) {
        window.open(url, "_blank")
    } else {
        ElMessage("暂无原文链接")
    }
}

function gotoYear(year) {
    let inputVal = encodeURIComponent(year)
    let optionVal = encodeURIComponent('Year')
    window.open(`./search.html?content=${inputVal}&type=${optionVal}`, "_self")
}

function gotoAuthor(author) {
    let inputVal = encodeURIComponent(author)
    let optionVal = encodeURIComponent('Author')
    window.open(`./search.html?content=${inputVal}&type=${optionVal}`, "_self")
}

function gotoKeyword(keyword) {
    let inputVal = encodeURIComponent(keyword)
    let optionVal = encodeURIComponent('Keywords')
    window.open(`./search.html?content=${inputVal}&type=${optionVal}`, "_self")
}

function fetchPDF(paperid) {
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
                    <div v-if="carddata['_source']['abstract'] && carddata['_source']['abstract'].length !== 0"
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
                    <div style="margin: 40px 20px 10px 20px;"
                        v-if="carddata['_source']['paper_id'] && carddata['paper_id'] !== ''">
                        <ElButton class="icon" @click.stop="fetchPDF(carddata['_source']['paper_id'])">
                            <el-icon>
                                <Document />
                            </el-icon>
                            <span>origin pdf</span>
                        </ElButton>
                        <ElButton class="icon" @click.stop="addLikedList(carddata['_source']['paper_id'])">
                            <ElImage :src="love_empty" fit="contain" style="width: 18px; margin: 0;"
                                v-if="!switchLikeStat" />
                            <ElImage :src="love_fill" fit="contain" style="width: 18px; margin: 0;" v-if="switchLikeStat" />
                            <span style="margin-left: 5px;">like</span>
                        </ElButton>
                    </div>
                </ElCard>
            </div>
        </div>
    </Transition>

    <div :style="{ height: '100vh', display: 'flex' }">
        <div
            :style="{ width: '100%', height: '100%', background: `url(${bgUrl})`, backgroundSize: 'cover', filter: 'blur(5px)' }" />
        <div style="position: absolute; width:100%; height: 100%; display: flex; min-width: 600px; min-height: 550px;">
            <ElCard
                style="filter: opacity(0.95); margin: auto; width: 80%; max-height: 95%; min-height: 80%; overflow-y: scroll;">
                <div style="display: flex; flex-direction: column; justify-content: center; width: 100%; margin-top: 40px;"
                    @mouseenter="bgBlur = true" @mouseleave="bgBlur = false">
                    <div style="position: absolute; left: 10px; top: 10px; display: flex;">
                        <ElButton @click="goBack" class="login-btn" size="large">
                            <el-icon>
                                <Back />
                            </el-icon>
                        </ElButton>
                        <ElButton @click="logout" class="logout" size="large">
                            log out
                        </ElButton>
                    </div>

                    <div style="text-align: center; margin:auto; margin-top: 20px;">
                        <ElAvatar style="height: 80px; width: 80px; font-size: 18px; font-size: 30px;" class="profile">{{
                            username[0] }}
                        </ElAvatar>
                    </div>
                    <div style="text-align: center; margin: auto; font-size: 40px; font-weight: 600; margin-top: 40px;"
                        class="profile">
                        Hello, {{ username }}!
                    </div>

                    <div
                        style="display: flex; margin-top: 30px; align-items: center; justify-content: center; flex-direction: column;">
                        <ElDivider border-style="dotted" style="width: 80%;"><span
                                style="font-size: 20px; font-weight: 600; color: gray;">liked papers</span></ElDivider>

                        <div class="clicked" v-for="paperid in liked"
                            style="width: 75%; border-radius: 10px; padding-left: 40px; padding-right: 40px; padding-top: 20px; padding-bottom: 20px;"
                            @click="showDetailFunc(paperid['ID'])">
                            <div class="title" style="font-size: larger; line-height: 1.6em;">
                                {{ paperid['Title'] }}
                            </div>
                        </div>

                        <ElDivider border-style="dotted" style="width: 80%;" />
                    </div>

                    <!-- <div style="width: 100%; position: absolute; bottom: 10px; display: flex; justify-content: center;"> -->
                    <div style="width: 100%; margin-top: 20px; display: flex; justify-content: center;">
                        <ElImage style="width: 30%; margin-top: 10px;" :src="LOGO" fit="contain" />
                    </div>
                </div>
            </ElCard>
    </div>
</div></template>