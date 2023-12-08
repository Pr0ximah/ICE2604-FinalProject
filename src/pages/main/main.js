import { createApp } from 'vue'
import 'element-plus/dist/index.css'
import '/src/style/default.css'
import ElementPlus from 'element-plus'
import App from './main.vue'

const app = createApp(App);
app.use(ElementPlus).mount('#app');