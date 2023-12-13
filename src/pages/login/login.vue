<script setup>
import { ElButton, ElCard, ElImage, ElInput, ElText, ElMessage } from 'element-plus'
import { ref } from 'vue'
import { User, Lock, Back } from '@element-plus/icons-vue'
import { useCookies } from 'vue3-cookies'
import LOGO from "@/assets/LOGO_DARK.png"
import API from '../../components/axios_instance'

const bgUrl = '/HOMEPAPERS/HOMEPAPER12.png'
let bgBlur = ref(true)
const username = ref("")
const passwd = ref("")
const { cookies } = useCookies()

function backToHome() {
    window.open("./", "_self")
}

function login() {
    if (username.value === '') {
        ElMessage("Please input username.")
        return
    }
    if (passwd.value === '') {
        ElMessage("Please input password.")
        return
    }
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username.value)
    const pwd = encodeURIComponent(passwd.value)
    API({
        url: base + `/login/${usrname}&${pwd}`,
        method: 'post'
    }).then((e) => {
        if (e.data) {
            localStorage.setItem('M_sc_username', username.value)
            cookies.set('M_sc_login_flag', true)
            window.history.go(-1)
        } else {
            ElMessage("User does not exist or the password is wrong! Please try again.")
        }
    }).catch(() => {
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

function goBack() {
    window.history.go(-1)
}
</script>

<template>
    <div :style="{ height: '100vh', display: 'flex' }">
        <div
            :style="{ width: '100%', height: '100%', background: `url(${bgUrl})`, backgroundSize: 'cover', filter: bgBlur ? 'blur(6px)' : '', transition: 'all 0.8s' }" />
        <div style="position: absolute; width:100%; height: 100%; display: flex;">
            <ElCard
                style="margin: auto; filter: opacity(0.87); width: 60%; min-height: 60%; display: flex; flex-direction: column; justify-content: center; min-width: 600px;"
                @mouseenter="bgBlur = true" @mouseleave="bgBlur = false">
                <ElButton @click="goBack" class="login-btn"
                    style="position: absolute; left: 10px; top: 10px;" size="large">
                    <el-icon>
                        <Back />
                    </el-icon>
                </ElButton>
                <div style="width: 100%; text-align: center; margin-top: 50px;">
                    <ElText class="login-title" tag="b" size="large" style="font-size: 40px;"> Sign in to M Scholar
                    </ElText>
                </div>
                <div
                    style="width: 80%; text-align: center; margin: auto; margin-top: 50px; display: flex; flex-direction: row; justify-content: center;">
                    <ElText tag="b" size="large" style="min-width: 100px; margin-right: 10px;">Username: </ElText>
                    <ElInput @keydown.enter="login" class="login-input" size="large" v-model="username"
                        placeholder="username" style="width: 40%; font-size:18px;">
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
                    <ElInput @keydown.enter="login" show-password class="login-input" size="large" v-model="passwd"
                        placeholder="password" style="width: 40%; font-size:18px;">
                        <template #prefix>
                            <el-icon>
                                <Lock />
                            </el-icon>
                        </template>
                    </ElInput>
                </div>
                <div
                    style="width: 35%; height: 12%; text-align: center; margin: auto; margin-top: 50px; margin-bottom: 100px; display: flex; flex-direction: row; justify-content: center;">
                    <ElButton class="login-btn" style="width: 100%; height: 100%;" @click="login">Sign in</ElButton>
                </div>
                <div style="width: 100%; position: absolute; bottom: 10px; display: flex; justify-content: center;">
                    <ElImage style="width: 30%; margin-top: 10px;" :src="LOGO" fit="contain" />
                </div>
            </ElCard>
        </div>
    </div>
</template>