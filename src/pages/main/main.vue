<script setup>
import { ElButton, ElContainer, ElIcon, ElImage, ElInput, ElMain, ElRow, ElCol, ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue'
import { onMounted, ref } from 'vue'
import { useCookies } from 'vue3-cookies'
import LOGO from '/src/assets/LOGO.png'
import { verifyLoginStatus } from '../../components/account_func'

const wallpapercnt = 16
const enableAll = ref(false)
const wallpaperurl = '/HOMEPAPERS/HOMEPAPER' + String(Math.floor(Math.random() * wallpapercnt)) + '.png'
const url = wallpaperurl;
const { cookies } = useCookies()
const isSignIn = ref(false)
const username = ref("")

let searchOptionVal = ref("")
if (enableAll.value) {
  searchOptionVal.value = "All"
} else {
  searchOptionVal.value = "Title"
}
const input = ref("")

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
  if (!input.value) {
    ElMessage("The input is empty.")
    return
  } else {
    if (searchOptionVal.value === "Year" && !/^[0-9]*$/.test(input.value)) {
      ElMessage("Year can only be an integer.")
      return
    }
    gotoResult()
  }
}

function gotoResult() {
  let inputVal = encodeURIComponent(input.value)
  let optionVal = encodeURIComponent(searchOptionVal.value)
  window.open(`./search.html?content=${inputVal}&type=${optionVal}`, "_self")
}

function signin() {
  localStorage.setItem("M_sc_lastpage", window.location.href)
  window.open("./login.html", "_self")
}

function signup() {
  localStorage.setItem("M_sc_lastpage", window.location.href)
  window.open("./signup.html", "_self")
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

onMounted(() => {
  checkLoginStatus()
})
</script>

<template>
  <ElContainer style="height: 100%;">
    <ElMain :style="{ background: `url(${url})`, backgroundSize: 'cover' }" class="mainpage">
      <ElRow justify="center">
        <ElImage class="logo" :src="LOGO" />
      </ElRow>
      <div class="main">
        <ElRow :gutter="20" justify="center">
          <ElCol :span="3" style="max-width: 150px;">
            <ElSelect class="mainSelect" style="width: 100%;" v-model="searchOptionVal">
              <ElOptionGroup v-if="enableAll">
                <ElOption label="All" value="All" />
              </ElOptionGroup>
              <ElOptionGroup>
                <ElOption v-for="item in SearchOption" :label="item.value" :value="item.value" />
              </ElOptionGroup>
            </ElSelect>
          </ElCol>
          <ElCol :span="12" style="height: 48px;">
            <ElInput placeholder="Enter your search term" class="mainInput" v-model="input"
              style="height: 100%; font-size: large;" @keydown.enter=search>
              <template #append>
                <ElButton class="mainSearchBtn" style="height: 100%; width: 80px;" @click="search">
                  <ElIcon style="height: 100%;">
                    <Search />
                  </ElIcon>
                </ElButton>
              </template>
            </ElInput>
          </ElCol>
        </ElRow>
      </div>
      <div
        style="position:absolute; bottom: 30px; text-align: center; margin: auto; width: 98%; color: #ffffff; text-shadow: 1px 1px 1px black;">
        <div style="margin: auto"> SJTU ICE2604 Final Project </div>
        <div style="margin: auto"> © Course Group 10 </div>
      </div>

      <div v-if="!isSignIn" style="position: absolute; right: 20px; top: 20px;">
        <ElButton size="large" @click="signup" class="mainpage-signin-btn hasborder">sign up</ElButton>
        <ElButton size="large" @click="signin" class="mainpage-signin-btn">sign in</ElButton>
      </div>

      <div v-if="isSignIn" style="position: absolute; right: 20px; top: 20px; display: flex;">
        <!-- <ElText style="font-size: 20px; color: #ffffff; font-weight: 550; margin: auto; margin-right: 10px;"> Welcome, </ElText> -->
        <ElAvatar @click="gotoProfile" size="large" style="font-size: large;">{{ username[0] }} </ElAvatar>
      </div>
    </ElMain>
  </ElContainer>
</template>