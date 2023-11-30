<script setup>
import { ElButton, ElContainer, ElIcon, ElImage, ElInput, ElMain, ElRow, ElCol, ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue'
import { ref } from 'vue'
import LOGO from './assets/LOGO.png'
// import API from './components/axios_instance'

const imgurl = "https://www.cs.sjtu.edu.cn/~wang-xb/ieei/images/xinbing.jpg"
const wallpapercnt = 16
const enableAll = ref(false)
let wallpaperurl = './src/assets/HOMEPAPERS/HOMEPAPER' + String(Math.floor(Math.random() * wallpapercnt)) + '.png'
let xb_avaliable = ref(false)
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
    ElMessage("输入为空")
    return
  } else {
    if (searchOptionVal.value === "Year" && !/^[0-9]*$/.test(input.value)) {
      ElMessage("年份必须为数字")
      return
    }
    gotoResult()
  }
}

function gotoResult() {
  window.open(`../pages/search.html?content=${input.value}&type=${searchOptionVal.value}`, "_self")
}
</script>

<template>
  <ElContainer style="height: 100%;">
    <ElMain :style="{ backgroundSize: 'cover', backgroundImage: 'url(\'' + wallpaperurl + '\')' }" class="mainpage">
      <ElRow justify="center">
        <ElImage class="logo" :src="LOGO" />
      </ElRow>
      <div class="main">
        <ElRow :gutter="10" justify="center">
          <ElCol :span="10">
            <ElInput style="height: 45px; font-size: large;" v-model="input" placeholder="" @keydown.enter=search>
              <template #suffix>
                <ElSelect style="width: 50%; margin-left: auto;" v-model="searchOptionVal">
                  <ElOptionGroup v-if="enableAll">
                    <ElOption label="All" value="All" />
                  </ElOptionGroup>
                  <ElOptionGroup>
                    <ElOption v-for="item in SearchOption" :label="item.value" :value="item.value" />
                  </ElOptionGroup>
                </ElSelect>
              </template>
            </ElInput>
          </ElCol>
          <ElCol :span="2">
            <ElButton class="search-btn" style="height: 45px;" @click="search"> 搜索 <ElIcon>
                <Search />
              </ElIcon>
            </ElButton>
          </ElCol>
        </ElRow>
      </div>
      <!-- <div class="main" style="margin-top: 5%; padding: auto;">
        <ElRow justify="center">
          <ElButton class="default" @click="xb_avaliable = !xb_avaliable" size="large"> {{ xb_button_text }} </ElButton>
        </ElRow>
      </div>
      <transition name="el-zoom-in-top">
        <div class="main" v-show="xb_avaliable" style="padding: auto;">
          <ElRow justify="center">
            <ElImage :src="imgurl" fit="contain" style="margin: 5px;" />
          </ElRow>
        </div>
      </transition>
      <div>
        <ElButton class="default" @click="gotoResult"> test -- goto result page </ElButton>
      </div> -->
      <div style="position:absolute; bottom: 30px; text-align: center; margin: auto; width: 98%; color: #ffffff; text-shadow: 1px 1px 1px black;">
        <div style="margin: auto"> SJTU ICE2604 Final Project </div>
        <div style="margin: auto"> © Course Group 10 </div>
      </div>
    </ElMain>
  </ElContainer>
</template>
