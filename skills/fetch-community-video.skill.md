---
name: fetch-community-video
alias: 视频社区AI情报采集
version: 1.0
platform: universal
---

# 视频社区AI情报采集 Skill

## 描述
定时自动抓取Bilibili、TikTok、抖音等视频社区的AI相关内容，包括教程、工具推荐、热点资讯等，自动分类并输出为结构化表格。

## 输入参数
- 关键词（可选）
- 分类（可选）

## 输出
- 标题、简介、分类、来源、标签、直达链接的表格

## 主要流程
1. 通过API/爬虫获取最新AI相关视频内容
2. 自动分类、去重
3. 输出美观表格

## 适用场景
- 行业热点追踪
- 视频教程发现
- 新工具/Agent/Skill发现
