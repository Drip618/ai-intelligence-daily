---
name: fetch-github-hf
alias: Github&Huggingface情报采集
version: 1.0
platform: universal
---

# Github&Huggingface情报采集 Skill

## 描述
定时自动抓取Github、Huggingface平台最新AI相关项目、Agent、Skill、Workflow等信息，自动分类并输出为结构化表格。

## 输入参数
- 关键词（可选）
- 分类（可选）

## 输出
- 标题、简介、分类、来源、标签、直达链接的表格

## 主要流程
1. 通过API/爬虫获取最新内容
2. 自动分类、去重
3. 输出美观表格

## 适用场景
- 行业情报收集
- 新兴工具发现
- 自动化知识库建设
