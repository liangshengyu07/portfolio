# Portfolio - LIANGSHENGYU

## 在线预览

### 方案一：临时链接（立即可用）
在本地运行 `start-tunnel.sh` 脚本，生成临时公开链接：

```bash
bash start-tunnel.sh
```

这会启动本地服务器并通过 tunnelmole 暴露到公网，生成一个类似 `https://xxx.tunnelmole.net` 的链接。

**注意**：关闭终端后链接会失效，需要重新运行脚本。

### 方案二：GitHub Pages（永久链接）
1. 将所有文件（包括图片、视频、字体）上传到此仓库
2. 在仓库 Settings > Pages 中启用 GitHub Pages
3. 选择 `main` 分支作为源
4. 访问 `https://liangshengyu07.github.io/portfolio`

## 文件清单

### 已上传文件
- `index.html` - 主页面
- `fonts/google-fonts.css` - 字体样式
- `lib/react.js` - React 库

### 需要手动上传的文件
- `lib/react-dom.js` - ReactDOM 库
- `lib/babel.js` - Babel 编译器
- `lib/tailwind.js` - Tailwind CSS
- `lib/framer-motion.js` - Framer Motion 动画库
- `fonts/*.ttf` - 字体文件（12个）
- `videos/*.mp4` - 视频文件（3个）
- `dd1.png` ~ `dd6.png` - 担当办公截图
- `idc1.png` ~ `idc3.png` - IDC 知识库截图
- `melos/*.png` - Melos Studio 截图（8个）

## 如何手动上传文件

### 方法 1：通过 GitHub 网页上传
1. 打开 https://github.com/liangshengyu07/portfolio
2. 点击 "Add file" → "Upload files"
3. 选择要上传的文件或文件夹
4. 填写提交信息，点击 "Commit changes"

### 方法 2：通过 Git 命令行
```bash
# 克隆仓库
git clone https://github.com/liangshengyu07/portfolio.git
cd portfolio

# 复制所有文件到仓库目录
# 然后提交并推送
git add .
git commit -m "Add all portfolio assets"
git push origin main
```

### 方法 3：通过 GitHub Desktop
1. 下载并安装 GitHub Desktop
2. 克隆此仓库
3. 将文件拖入仓库文件夹
4. 提交并推送

## 技术栈

- React 18 (CDN)
- Tailwind CSS (CDN)
- Babel (CDN)
- Framer Motion (CDN)
- 自定义字体：Inter, Instrument Serif, Barlow

## 响应式设计

网站已针对移动端进行优化，支持手机和平板访问：
- 导航栏在移动端变为汉堡菜单
- 布局自动调整为单列
- 图片和文字大小自适应
- 堆叠卡片在移动端垂直排列

## 本地开发

直接在浏览器中打开 `index.html` 即可预览，所有资源均为本地引用，无需网络连接。

---

**联系方式**
- 期望职位：AIGC设计师
- 电话：15613677775
- 邮箱：45633310@qq.com
