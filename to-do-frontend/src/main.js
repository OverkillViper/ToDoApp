import './assets/style.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'

axios.defaults.baseURL = 'http://192.168.0.9:8000'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
