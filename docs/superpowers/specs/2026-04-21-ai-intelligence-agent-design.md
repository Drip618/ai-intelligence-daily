# 智能 AI 情报 Agent 设计文档

**创建日期:** 2026-04-21  
**作者:** AI Assistant  
**版本:** 1.0

---

## 1. 整体架构

采用 **分层架构 + 插件化** 设计，将系统分为：
- 用户交互层 (CLI/Webhook)
- 部署适配层 (本地/Docker/Serverless)
- 核心引擎 (主控制器、调度器、工作流编排)
- 插件层 (采集插件/处理插件/输出插件)
- 模型适配层 (OpenAI/Claude/通义千问/Ollama)
- 数据存储层 (JSON/YAML + 可选向量数据库)

---

## 2. 核心模块设计

### 2.1 模型适配器层 (`src/adapters/models/`)

**接口定义:**
```python
class BaseModelAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """生成文本响应"""
    
    @abstractmethod
    def classify(self, content: str, categories: list[str]) -> dict:
        """内容分类"""
    
    @abstractmethod
    def summarize(self, texts: list[str]) -> str:
        """总结内容"""
```

**已实现适配器:**
- `OpenAIAdapter` - 支持 GPT-4/3.5
- `ClaudeAdapter` - 支持 Claude 3 Opus/Sonnet/Haiku
- `QwenAdapter` - 支持通义千问
- `OllamaAdapter` - 支持本地 Llama/Mistral 等

**配置示例:**
```yaml
model:
  provider: openai
  api_key: ${OPENAI_API_KEY}
  model_name: gpt-4-turbo
  temperature: 0.7
```

---

### 2.2 采集插件层 (`src/plugins/fetchers/`)

每个采集器实现统一接口：
```python
class BaseFetcher(ABC):
    @abstractmethod
    def fetch(self, keywords: list[str] = None) -> list[Item]:
        """采集数据"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """采集器名称"""
```

**已实现采集器:**
- `GithubFetcher` - Github API + GraphQL
- `HuggingfaceFetcher` - HF Hub API
- `BilibiliFetcher` - Bilibili API
- `TikTokFetcher` - 网页爬取
- `DouyinFetcher` - 网页爬取

---

### 2.3 存储层 (`src/storage/`)

**知识库结构:**
```
data/
├── knowledge/
│   ├── short_term/      # 短期记忆（本周）
│   ├── long_term/       # 长期记忆
│   └── skills/          # 沉淀的技能库
├── cache/               # 缓存数据
└── config.yaml          # 全局配置
```

---

### 2.4 推送插件层 (`src/plugins/pushers/`)

统一推送接口：
```python
class BasePusher(ABC):
    @abstractmethod
    def push(self, content: str, **kwargs) -> bool:
        """推送内容"""
```

**已实现推送器:**
- `EmailPusher` - SMTP 邮件
- `WeComPusher` - 企业微信 Webhook
- `DingTalkPusher` - 钉钉 Webhook
- `FeishuPusher` - 飞书 Webhook
- `TelegramPusher` - Telegram Bot API

---

### 2.5 部署适配层 (`deploy/`)

三种部署模板：
- `local/` - 本地运行 + crontab/systemd
- `docker/` - Dockerfile + docker-compose
- `serverless/` - 云函数配置（阿里云 FC/AWS Lambda）

---

## 3. 数据流

```
定时任务触发
    ↓
[1] 并行采集（各 fetcher 同时运行）
    ↓
[2] 内容合并 + 去重（基于 URL/标题 hash）
    ↓
[3] AI 分类 + 标签（调用模型适配器）
    ↓
[4] 更新知识库（短期→长期）
    ↓
[5] 格式化输出（Markdown 表格）
    ↓
[6] 多通道推送（并行发送到各渠道）
    ↓
[7] 日志记录 + 自我进化（定期执行）
```

---

## 4. 项目结构

```
数据收集1.0/
├── src/
│   ├── core/                    # 核心引擎
│   │   ├── agent.py             # IntelligenceAgent 主类
│   │   ├── scheduler.py         # 定时任务调度
│   │   └── workflow.py          # 工作流编排
│   ├── adapters/
│   │   └── models/              # 模型适配器
│   │       ├── base.py
│   │       ├── openai_adapter.py
│   │       ├── claude_adapter.py
│   │       ├── qwen_adapter.py
│   │       └── ollama_adapter.py
│   ├── plugins/
│   │   ├── fetchers/            # 采集插件
│   │   │   ├── base.py
│   │   │   ├── github.py
│   │   │   ├── huggingface.py
│   │   │   └── video_platforms.py
│   │   └── pushers/             # 推送插件
│   │       ├── base.py
│   │       ├── email.py
│   │       ├── webhook.py
│   │       └── telegram.py
│   ├── storage/
│   │   ├── knowledge_base.py    # 知识库管理
│   │   └── cache.py             # 缓存管理
│   ├── formatter.py             # 格式化引擎
│   └── utils.py                 # 工具函数
├── deploy/
│   ├── local/
│   │   └── run.sh
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── serverless/
│       └── config.yaml
├── data/                        # 数据存储
│   └── .gitkeep
├── config/
│   └── default.yaml             # 默认配置
├── tests/                       # 测试代码
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 5. 关键技术选型

| 模块 | 技术 | 理由 |
|------|------|------|
| AI 框架 | LangChain | 标准化模型接口，生态丰富 |
| 定时调度 | APScheduler | 支持 cron 表达式，灵活可靠 |
| HTTP 请求 | httpx | 异步支持，性能好 |
| 网页爬取 | BeautifulSoup4 + Playwright | 静态+动态页面全覆盖 |
| 配置管理 | PyYAML + python-dotenv | 灵活配置+环境变量 |
| 日志 | loguru | 简单易用，功能强大 |
| 测试 | pytest | Python 标准测试框架 |

---

## 6. 部署方案

### 6.1 本地运行
- 使用 crontab 或 systemd 定时任务
- 适合个人使用或小规模部署

### 6.2 Docker 部署
- 提供 Dockerfile 和 docker-compose.yml
- 适合生产环境，易于扩展和维护

### 6.3 Serverless 部署
- 阿里云 FC / AWS Lambda
- 按需运行，零运维，适合间歇性任务

---

## 7. 扩展性设计

### 7.1 新增模型适配器
只需实现 `BaseModelAdapter` 接口，在配置文件中添加配置即可

### 7.2 新增采集器
只需实现 `BaseFetcher` 接口，在配置文件中注册即可

### 7.3 新增推送渠道
只需实现 `BasePusher` 接口，在配置文件中注册即可

### 7.4 存储层升级
从 JSON/YAML 升级到向量数据库（如 Chroma/Faiss）无需修改核心代码，只需替换存储适配器
