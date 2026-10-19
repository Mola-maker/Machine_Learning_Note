import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
// GitHub Pages 项目站：base 必须等于仓库名
export default defineConfig({ plugins: [react()], base: '/Machine_Learning_Note/' })
