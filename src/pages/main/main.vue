<script setup>
import { ElButton, ElContainer, ElIcon, ElImage, ElInput, ElMain, ElRow, ElCol, ElMessage } from 'element-plus';
import { Search } from '@element-plus/icons-vue'
import { ref } from 'vue'
import LOGO from '/src/assets/LOGO.png'
// import API from './components/axios_instance'

const wallpapercnt = 16
const enableAll = ref(false)
const wallpaperurl = '/HOMEPAPERS/HOMEPAPER' + String(Math.floor(Math.random() * wallpapercnt)) + '.png'
const url = wallpaperurl;
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
  let inputVal = encodeURIComponent(input.value)
  let optionVal = encodeURIComponent(searchOptionVal.value)
  window.open(`./search.html?content=${inputVal}&type=${optionVal}`, "_self")
}
</script>

<template>
  <ElContainer style="height: 100%;">
    <ElMain :style="{ background: `url(${url})`, backgroundSize: 'cover' }" class="mainpage">
      <ElRow justify="center">
        <ElImage class="logo" :src="LOGO" />
      </ElRow>
      <div class="main">
        <ElRow :gutter="20" justify="center">
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
          <ElCol :span="1.2">
            <ElButton class="search-btn" style="height: 45px;" @click="search"> 搜索 <ElIcon>
                <Search />
              </ElIcon>
            </ElButton>
          </ElCol>
        </ElRow>
      </div>
      <div
        style="position:absolute; bottom: 30px; text-align: center; margin: auto; width: 98%; color: #ffffff; text-shadow: 1px 1px 1px black;">
        <div style="margin: auto"> SJTU ICE2604 Final Project </div>
        <div style="margin: auto"> © Course Group 10 </div>
      </div>
    </ElMain>
  </ElContainer>
</template>