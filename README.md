# douyin-videos

抖音视频归档库（GitHub Pages 自动托管）。

## 目录规则

- `videos/<日期>-<slug>/index.html` — 该视频的播放页
- `videos/<日期>-<slug>/video.mp4` — 视频原片
- 根目录 `index.html` — 视频列表页

## 容量规则

- 单个视频 **<= 100MB** 才入库（GitHub 单文件硬上限）
- 超过 100MB 的视频不放 GitHub，改用临时链接 + 本地原片

## 访问

https://superboy0303.github.io/douyin-videos/
