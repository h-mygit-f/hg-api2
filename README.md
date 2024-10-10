# Hugging Face API 代理服务

这是一个使用 Flask 构建的 Hugging Face API 代理服务。它允许您使用类似 OpenAI API 的格式来访问 Hugging Face 的模型。

## 功能

- 支持多种 Hugging Face 模型
- 兼容 OpenAI API 格式的请求
- 支持流式和非流式响应
- Docker 容器化部署

## 快速开始

1. 克隆此仓库：
   ```bash
   git clone https://github.com/your-username/huggingface-api-proxy.git
   cd huggingface-api-proxy
   ```

2. 创建 `.env` 文件并设置您的 API 密钥：
   ```bash
   HUGGINGFACE_API_KEY=your_actual_huggingface_api_key
   API_KEY=your_actual_custom_api_key
   ```

3. 使用 Docker Compose 构建和运行服务：
   ```bash
   docker-compose up --build
   ```

4. 服务现在应该在 `http://localhost:5023` 上运行。

## API 使用

发送 POST 请求到 `/v1/chat/completions` 端点，格式如下：