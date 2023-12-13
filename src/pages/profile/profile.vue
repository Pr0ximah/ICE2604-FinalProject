<script setup>
import { ElButton, ElCard, ElImage, ElInput, ElText, ElMessage } from 'element-plus'
import { ref, onMounted } from 'vue'
import { User, Lock, Back } from '@element-plus/icons-vue'
import { useCookies } from 'vue3-cookies'
import LOGO from "@/assets/LOGO_DARK.png"
import API from '../../components/axios_instance'

const bgUrl = '/HOMEPAPERS/HOMEPAPER2.png'
const { cookies } = useCookies()
const username = ref("")

function checkLoginStatus() {
    if (cookies.get('M_sc_login_flag') !== null) {
        username.value = localStorage.getItem("M_sc_username")
        return true
    } else {
        window.open('./login.html', '_self')
        return false
    }
}

onMounted(() => {
    checkLoginStatus()
})

function goBack() {
    window.history.go(-1)
}

function logout() {
    localStorage.removeItem('M_sc_username')
    cookies.remove('M_sc_login_flag')
    goBack()
}
</script>

<template>
    <div :style="{ height: '100vh', display: 'flex' }">
        <div
            :style="{ width: '100%', height: '100%', background: `url(${bgUrl})`, backgroundSize: 'cover', filter: 'blur(5px)' }" />
        <div style="position: absolute; width:100%; height: 100%; display: flex;">
            <ElCard
                style="margin: auto; filter: opacity(0.95); width: 80%; min-height: 80%; display: flex; flex-direction: column; justify-content: center; min-width: 600px;"
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

                <div style="text-align: center; margin:auto;">
                    <ElAvatar style="height: 80px; width: 80px; font-size: 18px;" class="profile">{{ username }} </ElAvatar>
                </div>
                <div style="text-align: center; margin: auto; font-size: 40px; font-weight: 600; margin-top: 40px;"
                    class="profile">
                    Hello, {{ username }}!
                </div>

                <div
                    style="display: flex; margin-top: 30px; align-items: center; justify-content: center; flex-direction: column;">
                    <ElDivider border-style="dotted" style="width: 80%;"><span
                            style="font-size: 20px; font-weight: 600; color: gray;">liked paper</span></ElDivider>

                    <ElDivider border-style="dotted" style="width: 80%;" />
                </div>

                <div style="width: 100%; position: absolute; bottom: 10px; display: flex; justify-content: center;">
                    <ElImage style="width: 30%; margin-top: 10px;" :src="LOGO" fit="contain" />
                </div>
            </ElCard>
        </div>
    </div>
</template>