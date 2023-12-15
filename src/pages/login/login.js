import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/style/default.css'
import App from './login.vue'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#login')