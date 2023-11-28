<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElRow, ElCol, ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue'
import { nextTick, ref, reactive } from 'vue'
import LOGO from './assets/LOGO.png'
import API from './components/axios_instance'

const imgurl = "https://www.cs.sjtu.edu.cn/~wang-xb/ieei/images/xinbing.jpg"
const wallpapercnt = 16
let wallpaperurl = './src/assets/HOMEPAPERS/HOMEPAPER' + String(Math.floor(Math.random() * wallpapercnt)) + '.png'
let xb_avaliable = ref(false)
let xb_button_text = ref("点我！")
const input = ref("")

function search() {
  if (!input.value) {
    ElMessage("输入为空")
    return
  } else {
    window.open(`../pages/search.html?search=${input.value}`, "_self")
  }
}

function gotoResult() {
  window.open(`../pages/search.html?search=${input.value}`, "_self")
}
</script>

<template>
  <ElContainer style="height: 100%;">
    <ElMain
      :style="{backgroundSize: 'cover', backgroundImage: 'url(\'' + wallpaperurl + '\')'}"
      class="mainpage">
      <ElRow justify="center">
        <ElImage class="logo" :src="LOGO" />
      </ElRow>
      <div class="main">
        <ElRow :gutter="10" justify="center">
          <ElCol :span="10">
            <ElInput style="height: 40px;" v-model="input" placeholder="" @keydown.enter=search></ElInput>
          </ElCol>
          <ElCol :span="2">
            <ElButton class="search-btn" style="height: 40px;" @click="search"> 搜索 <ElIcon>
                <Search />
              </ElIcon>
            </ElButton>
          </ElCol>
        </ElRow>
      </div>
      <div class="main" style="margin-top: 5%; padding: auto;">
        <ElRow justify="center">
          <!-- <ElButton class="default" @click="xb_avaliable = !xb_avaliable" size="large"> {{ xb_button_text }} </ElButton> -->
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
      </div>
    </ElMain>
  </ElContainer>
</template>
