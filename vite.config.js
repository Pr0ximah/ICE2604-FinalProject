import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'node:path'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue()
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~@': fileURLToPath(new URL('./src', import.meta.url)),
    }
  },
  build: {
    emptyOutDir: true,
    rollupOptions: {
      input: {
        index: resolve(__dirname, '/index.html'),
        search: resolve(__dirname, '/search.html'),
        login: resolve(__dirname, '/login.html'),
        signup: resolve(__dirname, '/signup.html'),
        profile: resolve(__dirname, '/profile.html'),
      }
    }
  },
  server: {
    host: 'localhost',
    port: 17001,
    https: false,
    proxy: {
      '/data_proxy': {
        target: 'http://127.0.0.1:8000/api_port/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/data_proxy/, '')
      }
    }
  }
})