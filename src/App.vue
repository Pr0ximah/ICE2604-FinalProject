<script setup>
import { ElButton, ElContainer, ElHeader, ElIcon, ElImage, ElInput, ElMain, ElRow, ElCol, ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue'
import { VueElement, nextTick, ref, reactive } from 'vue'
import LOGO from './assets/LOGO.png'
import API from './components/axios_instance'

const imgurl = "https://www.cs.sjtu.edu.cn/~wang-xb/ieei/images/xinbing.jpg"
let xb_avaliable = ref(false)
let xb_button_text = ref("点我！")
const input = ref("")
let pic_url = reactive({url: ""})

function search() {
  if (!input.value) {
    ElMessage("输入为空")
    return
  } else {
    window.open(`https://www.baidu.com/s?wd=${input.value}`)
  }
}

function getAPItest() {
  API({
    url:'/proxy/v2/random',
    method: 'get'
  }).then((res)=>{
    const tar = res['data']['url']
    console.log(tar)
    pic_url.url = new URL(tar).href
    nextTick()
  }).catch(()=>{
    ElMessage("Get error")
  })
}

function gotoResult() {
  window.open(`../pages/search/index.html?search=${input.value}`, "_self")
}
</script>

<template>
  <ElContainer style="height: 100%;">
    <ElMain
      style="background-image: url(https://picx.zhimg.com/80/v2-36d4626179b21ede507f08593329aa22_1440w.webp?source=1def8ac); background-size: cover;">
      <ElRow justify="center">
        <ElImage class="logo" :src="LOGO" />
      </ElRow>
      <div class="main">
        <ElRow :gutter="10" justify="center">
          <ElCol :span="10">
            <ElInput style="height: 40px;" v-model="input" placeholder="百度一下" @keydown.enter=search></ElInput>
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
        <ElButton class="default" @click="gotoResult"> try! </ElButton>
        <ElButton class="default" @click="getAPItest"> press </ElButton>
        <ElImage :src="pic_url.url" fit="contain" style="margin: 5px;" v-if="pic_url.url !== ''"/>
      </div>
    </ElMain>
  </ElContainer>
</template>
