from flask import Flask, request, jsonify, Response
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import time
import json
from functools import wraps

# 加载 .env 文件
load_dotenv()

# 从 .env 文件获取 API keys
huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
api_key = os.getenv("API_KEY")

app = Flask(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get('Authorization')
        if provided_key:
            if provided_key.startswith("Bearer "):
                provided_key = provided_key.split("Bearer ")[1]
            if provided_key == api_key:
                return f(*args, **kwargs)
        return jsonify({"error": "Invalid or missing API key"}), 401
    return decorated

@app.route('/v1/chat/completions', methods=['POST'])
@require_api_key
def chat_completions():
    data = request.json
    messages = data.get('messages', [])
    model = data.get('model', 'gpt2')  # 默认使用 gpt2，但允许客户端指定任何模型
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 8196)
    top_p = min(max(data.get('top_p', 0.9), 0.0001), 0.9999)  # 确保 top_p 在有效范围内
    stream = data.get('stream', False)

    try:
        # 为每个请求创建一个新的 InferenceClient 实例
        client = InferenceClient(model=model, api_key=huggingface_api_key)

        response = client.chat.completions.create(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream
        )

        if stream:
            def generate():
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield f"data: {json.dumps({'choices': [{'delta': {'content': content}}]})}\n\n"
                yield "data: [DONE]\n\n"
            return Response(generate(), mimetype='text/event-stream')
        else:
            content = response.choices[0].message.content
            return jsonify({
                'id': f'chatcmpl-{int(time.time())}',
                'object': 'chat.completion',
                'created': int(time.time()),
                'model': model,
                'choices': [
                    {
                        'index': 0,
                        'message': {
                            'role': 'assistant',
                            'content': content
                        },
                        'finish_reason': 'stop'
                    }
                ],
                'usage': {
                    'prompt_tokens': -1,
                    'completion_tokens': -1,
                    'total_tokens': -1
                }
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)