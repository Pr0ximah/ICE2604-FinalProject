import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@/style/default.css'
import App from './profile.vue'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#profile')