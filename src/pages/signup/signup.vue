<script setup>
import { ElButton, ElCard, ElImage, ElInput, ElMessage, ElText } from 'element-plus'
import { ref } from 'vue'
import { User, Lock, Back } from '@element-plus/icons-vue'
import { useCookies } from 'vue3-cookies'
import LOGO from "@/assets/LOGO_DARK.png"
import { signup_inner, backToHome, goBack } from '../../components/account_func'

const bgUrl = '/HOMEPAPERS/HOMEPAPER12.png'
let bgBlur = ref(true)
const username = ref("")
const passwd = ref("")
const repasswd = ref("")
const { cookies } = useCookies()
const showSignResult = ref(false)
const secToLeave = ref(3)

async function signup() {
    signup_inner(username.value, passwd.value, repasswd.value).then(e => {
        if (e.data) {
            showSignResult.value = true;
            setInterval(() => {
                if (secToLeave.value == 1) {
                    clearInterval()
                    goBack()
                }
                secToLeave.value -= 1
            }, 1000)
        }
    })
}
</script>

<template>
    <div :style="{ height: '100vh', display: 'flex' }">
        <div
            :style="{ width: '100%', height: '100%', background: `url(${bgUrl})`, backgroundSize: 'cover', filter: bgBlur ? 'blur(6px)' : '', transition: 'all 0.8s' }" />
        <div style="position: absolute; width:100%; height: 100%; display: flex;">
            <ElCard
                style="margin: auto; filter: opacity(0.87); width: 60%; min-height: 75%; display: flex; flex-direction: column; justify-content: center; min-width: 600px;"
                @mouseenter="bgBlur = true" @mouseleave="bgBlur = false">
                <ElButton @click="goBack" class="login-btn" style="position: absolute; left: 10px; top: 10px;" size="large">
                    <el-icon>
                        <Back />
                    </el-icon>
                </ElButton>
                <div style="width: 100%; text-align: center; margin-top: 50px;" v-if="!showSignResult">
                    <ElText class="login-title" tag="b" size="large" style="font-size: 40px;"> Sign up to M Scholar
                    </ElText>
                </div>
                <div style="width: 80%; text-align: center; margin: auto; margin-top: 50px; display: flex; flex-direction: row; justify-content: center;"
                    v-if="!showSignResult">
                    <ElText tag="b" size="large" style="min-width: 110px; margin-right: 10px;">Username: </ElText>
                    <ElInput @keydown.enter="signup" class="login-input" size="large" v-model="username"
                        placeholder="username" style="width: 40%; font-size:18px;">
                        <template #prefix>
                            <el-icon>
                                <User />
                            </el-icon>
                        </template>
                    </ElInput>
                </div>
                <div style="width: 80%; text-align: center; margin: auto; margin-top: 30px; display: flex; flex-direction: row; justify-content: center;"
                    v-if="!showSignResult">
                    <ElText tag="b" size="large" style="min-width: 110px; margin-right: 10px;">Password: </ElText>
                    <ElInput @keydown.enter="signup" show-password class="login-input" size="large" v-model="passwd"
                        placeholder="password" style="width: 40%; font-size:18px;">
                        <template #prefix>
                            <el-icon>
                                <Lock />
                            </el-icon>
                        </template>
                    </ElInput>
                </div>
                <div style="width: 80%; text-align: center; margin: auto; margin-top: 30px; display: flex; flex-direction: row; justify-content: center;"
                    v-if="!showSignResult">
                    <ElText tag="b" size="large" style="min-width: 110px; margin-right: 10px;">Re-enter pwd: </ElText>
                    <ElInput @keydown.enter="signup" show-password class="login-input" size="large" v-model="repasswd"
                        placeholder="confirm password" style="width: 40%; font-size:18px;">
                        <template #prefix>
                            <el-icon>
                                <Lock />
                            </el-icon>
                        </template>
                    </ElInput>
                </div>
                <div style="width: 35%; height: 12%; text-align: center; margin: auto; margin-top: 50px; display: flex; flex-direction: row; justify-content: center; margin-bottom: 100px;"
                    v-if="!showSignResult">
                    <ElButton class="login-btn" style="width: 100%; height: 100%;" @click="signup">Sign up</ElButton>
                </div>

                <div v-if="showSignResult"
                    style="height: 70%; margin-bottom: 100px; display: flex; align-items: center; justify-content: center;">
                    <ElResult icon="success" title="Sign up sucessfully!"
                        :sub-title="`Return to main page in ${secToLeave} seconds.`"
                        style="transform: scale(1.1); font-weight: 550;" />
                </div>

                <div style="width: 100%; position: absolute; bottom: 10px; display: flex; justify-content: center;">
                    <ElImage style="width: 30%; margin-top: 10px;" :src="LOGO" fit="contain" />
                </div>
            </ElCard>
        </div>
    </div>
</template>