import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'node:path'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        login: resolve(__dirname, 'pages/search/index.html')
      }
    }
  },
  server: {
    proxy: {
      '/proxy' : {
        target: 'https://random-d.uk/api',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/proxy/, '')
      }
    }
  }
})