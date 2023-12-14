import API from './axios_instance'
import { useCookies } from 'vue3-cookies'
import { ElMessage } from 'element-plus'

export {
    login_inner,
    signup_inner,
    backToHome,
    goBack,
}

const { cookies } = useCookies()

async function signup_inner(username, passwd, repasswd) {
    if (username === '') {
        ElMessage("Please input username.")
        return
    }
    if (passwd === '') {
        ElMessage("Please input password.")
        return
    }
    if (passwd !== repasswd) {
        ElMessage("Two passwords is inconsistent. Please try again.")
        return
    }
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username)
    const pwd = encodeURIComponent(passwd)
    return API({
        url: base + `/signup/${usrname}&${pwd}`,
        method: 'post'
    }).then((e) => {
        console.log(e)
        if (e.data) {
            localStorage.setItem('M_sc_username', username)
            cookies.set('M_sc_login_flag', true)
        } else {
            ElMessage("User already exist! Please change the username and try again.")
        }
        return e
    }).catch(() => {
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

async function login_inner(username, passwd) {
    if (username === '') {
        ElMessage("Please input username.")
        return
    }
    if (passwd === '') {
        ElMessage("Please input password.")
        return
    }
    const base = process.env.NODE_ENV === "development" ? "/data_proxy" : "/api"
    const usrname = encodeURIComponent(username)
    const pwd = encodeURIComponent(passwd)
    return API({
        url: base + `/login/${usrname}&${pwd}`,
        method: 'post'
    }).then((e) => {
        if (e.data) {
            localStorage.setItem('M_sc_username', username)
            cookies.set('M_sc_login_flag', true)
        } else {
            ElMessage("User does not exist or the password is wrong! Please try again.")
        }
        return e
    }).catch(() => {
        ElMessage("Oops! Internal server error. Try again later.")
    })
}

function backToHome() {
    window.open("./", "_self")
}

function goBack() {
    const url = localStorage.getItem("M_sc_lastpage")
    if (url) {
        window.open(url, '_self');
    } else {
        backToHome()
    }
}