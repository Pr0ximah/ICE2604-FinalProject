import { createApp } from 'vue'
import 'element-plus/dist/index.css'
import '@/style/default.css'
import ElementPlus from 'element-plus'
import Result from './result.vue'

createApp(Result).use(ElementPlus).mount('#result')