<script setup>
import { ElButton, ElCard, ElImage, ElInput, ElText } from 'element-plus'
import { ref } from 'vue'
import { User, Lock, Back } from '@element-plus/icons-vue'
import LOGO from "@/assets/LOGO_DARK.png"
const bgUrl = '/HOMEPAPERS/HOMEPAPER12.png'
let bgBlur = ref(true)
const username = ref("")
const passwd = ref("")

function login() {

}

function backToHome() {
    window.open("./", "_self")
}
</script>

<template>
    <div :style="{ height: '100vh', display: 'flex' }">
        <div
            :style="{ width: '100%', height: '100%', background: `url(${bgUrl})`, backgroundSize: 'cover', filter: bgBlur ? 'blur(6px)' : '', transition: 'all 0.8s' }" />
        <div style="position: absolute; width:100%; height: 100%; display: flex;">
            <ElCard
                style="margin: auto; filter: opacity(0.87); width: 60%; height: 60%; display: flex; flex-direction: column; justify-content: center;"
                @mouseenter="bgBlur = true" @mouseleave="bgBlur = false">
                <ElButton @click="backToHome" class="login-btn" style="position: absolute; left: 10px; top: 10px;" size="large">
                    <el-icon>
                        <Back />
                    </el-icon>
                </ElButton>
                <div style="width: 100%; text-align: center;">
                    <ElText class="login-title" tag="b" size="large" style="font-size: 40px;"> Sign in to M Scholar
                    </ElText>
                </div>
                <div
                    style="width: 80%; text-align: center; margin: auto; margin-top: 50px; display: flex; flex-direction: row; justify-content: center;">
                    <ElText tag="b" size="large" style="min-width: 100px; margin-right: 10px;">Username: </ElText>
                    <ElInput class="login-input" size="large" v-model="username" placeholder="usrname"
                        style="width: 40%; font-size:18px;">
                        <template #prefix>
                            <el-icon>
                                <User />
                            </el-icon>
                        </template>
                    </ElInput>
                </div>
                <div
                    style="width: 80%; text-align: center; margin: auto; margin-top: 30px; display: flex; flex-direction: row; justify-content: center;">
                    <ElText tag="b" size="large" style="min-width: 100px; margin-right: 10px;">Password: </ElText>
                    <ElInput show-password class="login-input" size="large" v-model="passwd" placeholder="password"
                        style="width: 40%; font-size:18px;">
                        <template #prefix>
                            <el-icon>
                                <Lock />
                            </el-icon>
                        </template>
                    </ElInput>
                </div>
                <div
                    style="width: 35%; height: 12%; text-align: center; margin: auto; margin-top: 50px; display: flex; flex-direction: row; justify-content: center;">
                    <ElButton class="login-btn" style="width: 100%; height: 100%;" @click="login">Sign in</ElButton>
                </div>
                <div style="width: 30%; text-align: center; margin: auto; margin-top: 50px;">
                <ElImage style="width: 100%;" :src="LOGO" fit="contain" />
            </div>
        </ElCard>
    </div>
</div></template>