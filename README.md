<div align='center'>
  <img src='./assets/sakura-overlay.svg' width='100%' alt='Animated falling sakura petals' />
</div>

<p align='center'>
  <img src='./assets/chibi-sakura-girl.svg' width='86' alt='sakura girl' />
  <img src='./assets/chibi-cloud-boy.svg' width='86' alt='cloud boy' />
  <img src='./assets/chibi-fox-cat.svg' width='86' alt='fox cat' />
  <img src='./assets/chibi-counter-host.svg' width='108' alt='counter host' />
  <img src='https://komarev.com/ghpvc/?username=Ltdaaa&label=Visitors&color=f38bb3&style=for-the-badge' alt='visitor counter' height='28' />
</p>

<p align='center'>
  <img src='./assets/rainbow-divider.svg' width='100%' alt='rainbow divider' />
</p>

<p align='center'><strong>Have a good day!</strong></p>

<div align='center'>
  <img src='./assets/sakura-overlay.svg' width='100%' alt='More falling sakura petals' />
</div>

## Deployment Guide

### 1. 创建和用户名同名仓库

1. 登录 GitHub，新建一个公开仓库。
2. 仓库名必须和你的用户名完全一致，这里就是 `Ltdaaa`。
3. 把 `output/github-profile-readme-ltdaaa/` 里的全部文件复制到那个仓库根目录，然后推送。

### 2. 开启仓库 GitHub Actions 权限

1. 进入仓库的 `Settings` -> `Actions` -> `General`。
2. 确认允许工作流运行，至少要让仓库内的 GitHub Actions 可以读写仓库内容。
3. 首次推送后，进入 `Actions` 页签手动运行一次 `Update Contribution Maze`，确认 `assets/contribution-maze.svg` 成功生成并提交。

### 3. 替换头像、图片链接、用户名的修改位置

1. 替换头像：修改 `README.md` 里左侧资料卡的 `./assets/avatar-slot.svg`，或者直接把这个 SVG 换成你自己的头像图片路径。
2. 替换风景大图链接：修改文末这张占位图的跳转地址和图片路径。
   当前写法是 `[![Landscape Placeholder](./assets/scenery-placeholder.svg)](https://example.com/replace-with-your-scenery-link)`。
3. 替换用户名：同步修改 `README.md` 中的 `Ltdaaa`、访问量计数器 URL 里的 `username=Ltdaaa`、以及 `.github/workflows/update-contribution-maze.yml` 里的 `PROFILE_USERNAME: Ltdaaa`。
4. 如果你想替换迷宫卡片标题、配色或文案，可编辑 `scripts/generate_contribution_maze.py` 后重新运行一次工作流。

## Landscape Link Placeholder

[![Landscape Placeholder](./assets/scenery-placeholder.svg)](https://example.com/replace-with-your-scenery-link)
