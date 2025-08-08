"""
现代化AI客户端 - 支持多提供商和流式响应
"""
import asyncio
import json
import time
from typing import Dict, List, Optional, AsyncGenerator, Callable
import aiohttp
import google.generativeai as genai
from openai import AsyncOpenAI

from .ai_types import (
    AIProviderConfig, ChatMessage, ChatCompletionRequest, 
    ChatCompletionResponse, ConnectionTestResult
)

class BaseAIClient:
    """AI客户端基类"""
    
    def __init__(self, config: AIProviderConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            headers=self.config.custom_headers or {}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_models(self):
        """获取模型列表"""
        raise NotImplementedError

    async def test_connection(self) -> ConnectionTestResult:
        """测试连接"""
        raise NotImplementedError

    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """聊天完成"""
        raise NotImplementedError

    async def stream_chat_completion(
        self,
        request: ChatCompletionRequest,
        on_chunk: Callable[[str], None]
    ) -> AsyncGenerator[str, None]:
        """流式聊天完成"""
        raise NotImplementedError

class OpenAICompatibleClient(BaseAIClient):
    """OpenAI兼容客户端（支持DeepSeek、通义千问、NewAPI等）"""
    
    def __init__(self, config: AIProviderConfig):
        super().__init__(config)
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout
        )
    
    async def get_models(self):
        """获取模型列表"""
        try:
            models = await self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"获取模型列表失败: {e}")
            return []

    async def test_connection(self) -> ConnectionTestResult:
        """测试连接"""
        start_time = time.time()
        try:
            models = await self.client.models.list()
            response_time = (time.time() - start_time) * 1000
            return ConnectionTestResult(
                success=True,
                response_time=response_time,
                model_count=len(models.data)
            )
        except Exception as e:
            return ConnectionTestResult(
                success=False,
                error=str(e)
            )
    
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """聊天完成"""
        try:
            # 转换消息格式
            messages = [
                {"role": msg.role, "content": msg.content} 
                for msg in request.messages
            ]
            
            response = await self.client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=False
            )
            
            return ChatCompletionResponse(
                id=response.id,
                model=response.model,
                choices=[{
                    "message": {
                        "role": choice.message.role,
                        "content": choice.message.content
                    },
                    "finish_reason": choice.finish_reason
                } for choice in response.choices],
                usage={
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                } if response.usage else None,
                created=response.created
            )
        except Exception as e:
            raise Exception(f"OpenAI兼容API调用失败: {str(e)}")
    
    async def stream_chat_completion(
        self, 
        request: ChatCompletionRequest,
        on_chunk: Callable[[str], None]
    ) -> AsyncGenerator[str, None]:
        """流式聊天完成"""
        try:
            messages = [
                {"role": msg.role, "content": msg.content} 
                for msg in request.messages
            ]
            
            stream = await self.client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    on_chunk(content)
                    yield content
                    
        except Exception as e:
            raise Exception(f"流式API调用失败: {str(e)}")

class GeminiClient(BaseAIClient):
    """Gemini客户端"""

    def __init__(self, config: AIProviderConfig):
        super().__init__(config)
        genai.configure(api_key=config.api_key)
        self.model = genai.GenerativeModel(config.model)

    async def get_models(self):
        """获取模型列表"""
        try:
            # Gemini的模型列表相对固定，返回常用模型
            return ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
        except Exception as e:
            print(f"获取Gemini模型列表失败: {e}")
            return ["gemini-1.5-flash"]

    async def test_connection(self) -> ConnectionTestResult:
        """测试连接"""
        start_time = time.time()
        try:
            # 发送一个简单的测试消息
            response = await asyncio.to_thread(
                self.model.generate_content, 
                "Hello"
            )
            response_time = (time.time() - start_time) * 1000
            return ConnectionTestResult(
                success=True,
                response_time=response_time
            )
        except Exception as e:
            return ConnectionTestResult(
                success=False,
                error=str(e)
            )
    
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """聊天完成"""
        try:
            # Gemini只需要用户消息，系统消息需要特殊处理
            user_messages = [msg.content for msg in request.messages if msg.role == "user"]
            prompt = "\n".join(user_messages)
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            return ChatCompletionResponse(
                id=f"gemini-{int(time.time())}",
                model=request.model,
                choices=[{
                    "message": {
                        "role": "assistant",
                        "content": response.text
                    },
                    "finish_reason": "stop"
                }],
                created=int(time.time())
            )
        except Exception as e:
            raise Exception(f"Gemini API调用失败: {str(e)}")
    
    async def stream_chat_completion(
        self, 
        request: ChatCompletionRequest,
        on_chunk: Callable[[str], None]
    ) -> AsyncGenerator[str, None]:
        """流式聊天完成"""
        # Gemini的流式实现较复杂，这里先实现非流式版本
        response = await self.chat_completion(request)
        content = response.choices[0]["message"]["content"]
        
        # 模拟流式输出
        words = content.split()
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            on_chunk(chunk)
            yield chunk
            await asyncio.sleep(0.05)  # 模拟延迟

class AIClientFactory:
    """AI客户端工厂"""
    
    @staticmethod
    def create_client(provider: str, config: AIProviderConfig) -> BaseAIClient:
        """创建AI客户端"""
        if provider == "gemini":
            return GeminiClient(config)
        else:
            # DeepSeek、通义千问、OpenAI、NewAPI都使用OpenAI兼容客户端
            return OpenAICompatibleClient(config)

class AIClientManager:
    """AI客户端管理器"""
    
    def __init__(self):
        self.clients: Dict[str, BaseAIClient] = {}
    
    def get_client(self, provider: str, config: AIProviderConfig) -> BaseAIClient:
        """获取或创建客户端"""
        if provider not in self.clients:
            self.clients[provider] = AIClientFactory.create_client(provider, config)
        return self.clients[provider]
    
    async def test_all_connections(self, configs: Dict[str, AIProviderConfig]) -> Dict[str, ConnectionTestResult]:
        """测试所有连接"""
        results = {}
        for provider, config in configs.items():
            if config.enabled and config.api_key:
                client = self.get_client(provider, config)
                async with client:
                    results[provider] = await client.test_connection()
            else:
                results[provider] = ConnectionTestResult(
                    success=False,
                    error="未启用或缺少API密钥"
                )
        return results
    
    async def close_all(self):
        """关闭所有客户端"""
        for client in self.clients.values():
            if hasattr(client, 'session') and client.session:
                await client.session.close()
        self.clients.clear()
