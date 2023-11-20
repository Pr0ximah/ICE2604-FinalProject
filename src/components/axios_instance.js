import axios from 'axios'

const API = axios.create({
    timeout: 8000
})

export default API