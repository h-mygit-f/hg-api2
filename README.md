# Hugging Face API 代理服务

这是一个使用 Flask 构建的 Hugging Face API 代理服务。它允许您使用类似 OpenAI API 的格式来访问 Hugging Face 的模型。目前来说只有Qwen/Qwen2.5-72B-Instruct 值得使用。

## 功能

- 支持多种 Hugging Face 模型
- 兼容 OpenAI API 格式的请求
- 支持流式和非流式响应
- Docker 容器化部署

## 快速开始

1. 克隆此仓库：
   ```bash
   git clone https://github.com/your-username/hg-api2
   cd hg-api2
   ```

2. 创建 `.env` 文件并设置您的 API 密钥,访问 https://huggingface.co/settings/tokens/new?globalPermissions=inference.serverless.write&tokenType=fineGrained 创建新的API token,确保选择了 inference.serverless.write 权限：
   ```bash
   HUGGINGFACE_API_KEY=your_actual_huggingface_api_key
   API_KEY=your_actual_custom_api_key
   ```

3. 使用 Docker Compose 构建和运行服务：
   ```bash
   docker-compose up -d
   ```

4. 服务现在应该在 `http://localhost:5023` 上运行。

5. 如果你要在newapi上使用，Base URL: `http://1.1.1.1:5023/v1/chat/completions` ，将1.1.1.1换成你自己的ip，模型：Qwen/Qwen2.5-72B-Instruct，密钥填写自己设定的 API_KEY。

