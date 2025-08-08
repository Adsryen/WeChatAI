"""
现代化AI管理器 - 基于新的配置架构
"""
import asyncio
import time
from typing import Dict, List, Optional, Callable, AsyncGenerator
from .ai_config import AIConfigManager
from .ai_client import AIClientManager, BaseAIClient
from .ai_types import (
    ChatMessage, ChatCompletionRequest, AIProvider,
    ConnectionTestResult
)

class ModernAIManager:
    """现代化AI管理器"""

    def __init__(self, config_manager=None):
        # 兼容旧的config_manager，同时支持新的AI配置
        self.legacy_config = config_manager
        self.ai_config = AIConfigManager()
        self.client_manager = AIClientManager()
        self.chat_histories: Dict[str, List[ChatMessage]] = {}

        # 如果有旧配置，迁移到新配置
        if config_manager:
            self._migrate_legacy_config()

    def _migrate_legacy_config(self):
        """迁移旧配置到新配置系统"""
        try:
            # 迁移API密钥
            for provider in ["deepseek", "gemini", "qianwen"]:
                api_key = self.legacy_config.get_api_key(provider)
                if api_key:
                    self.ai_config.set_api_key(provider, api_key)

            # 迁移系统提示词
            system_prompt = self.legacy_config.get_system_prompt()
            if system_prompt:
                self.ai_config.settings.system_prompt = system_prompt

            # 迁移默认模型
            default_model = self.legacy_config.config.get("default_model", "deepseek")
            if default_model in ["deepseek", "gemini", "qianwen"]:
                self.ai_config.settings.default_provider = AIProvider(default_model)

            # 迁移代理设置
            proxy = self.legacy_config.get_proxy()
            if proxy.get("http") or proxy.get("https"):
                for provider_name in self.ai_config.settings.providers:
                    self.ai_config.settings.providers[provider_name].proxy = proxy

            # 保存迁移后的配置
            self.ai_config.save_config()
            print("配置迁移完成")

        except Exception as e:
            print(f"配置迁移失败: {e}")

    def get_chat_history(self, group_name: str) -> List[ChatMessage]:
        """获取聊天历史"""
        if group_name not in self.chat_histories:
            system_prompt = self.ai_config.settings.system_prompt
            self.chat_histories[group_name] = [
                ChatMessage(role="system", content=system_prompt, timestamp=time.time())
            ]
        return self.chat_histories[group_name]

    def add_message(self, group_name: str, role: str, content: str):
        """添加消息到历史"""
        history = self.get_chat_history(group_name)
        message = ChatMessage(role=role, content=content, timestamp=time.time())
        history.append(message)

        # 保持历史记录在合理范围内
        max_length = self.ai_config.settings.max_history_length
        if len(history) > max_length + 1:  # +1 for system message
            # 保留系统消息和最近的消息
            system_msg = history[0]
            recent_msgs = history[-(max_length):]
            self.chat_histories[group_name] = [system_msg] + recent_msgs

    async def get_ai_response(self, message: str, group_name: str, provider: str = None) -> Optional[str]:
        """获取AI回复 - 现代化版本"""
        try:
            # 确定使用的提供商
            if not provider:
                provider = self.ai_config.settings.default_provider.value

            # 检查提供商配置
            config = self.ai_config.get_provider_config(provider)
            if not config or not config.enabled or not config.api_key:
                return f"提供商 {provider} 未配置或未启用"

            # 添加用户消息到历史
            self.add_message(group_name, "user", message)
            history = self.get_chat_history(group_name)

            # 创建请求
            request = ChatCompletionRequest(
                model=config.model,
                messages=history,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                stream=False
            )

            # 获取客户端并发送请求
            client = self.client_manager.get_client(provider, config)
            async with client:
                response = await client.chat_completion(request)

                if response.choices and response.choices[0]["message"]["content"]:
                    reply = response.choices[0]["message"]["content"].strip()
                    self.add_message(group_name, "assistant", reply)
                    return reply
                else:
                    return "AI 没有返回有效结果，请稍后再试"

        except Exception as e:
            print(f"AI调用失败: {str(e)}")
            return f"AI调用出错: {str(e)}"

    async def get_ai_response_stream(
        self,
        message: str,
        group_name: str,
        provider: str = None,
        on_chunk: Callable[[str], None] = None
    ) -> AsyncGenerator[str, None]:
        """获取流式AI回复"""
        try:
            # 确定使用的提供商
            if not provider:
                provider = self.ai_config.settings.default_provider.value

            # 检查提供商配置
            config = self.ai_config.get_provider_config(provider)
            if not config or not config.enabled or not config.api_key:
                yield f"提供商 {provider} 未配置或未启用"
                return

            # 添加用户消息到历史
            self.add_message(group_name, "user", message)
            history = self.get_chat_history(group_name)

            # 创建请求
            request = ChatCompletionRequest(
                model=config.model,
                messages=history,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                stream=True
            )

            # 获取客户端并发送流式请求
            client = self.client_manager.get_client(provider, config)
            full_response = ""

            async with client:
                async for chunk in client.stream_chat_completion(request, on_chunk or (lambda x: None)):
                    full_response += chunk
                    yield chunk

            # 添加完整回复到历史
            if full_response:
                self.add_message(group_name, "assistant", full_response)

        except Exception as e:
            print(f"流式AI调用失败: {str(e)}")
            yield f"AI调用出错: {str(e)}"

    async def test_connections(self) -> Dict[str, ConnectionTestResult]:
        """测试所有提供商连接"""
        enabled_configs = {
            name: config for name, config in self.ai_config.settings.providers.items()
            if config.enabled and config.api_key
        }
        return await self.client_manager.test_all_connections(enabled_configs)

    def get_available_providers(self) -> List[str]:
        """获取可用的提供商列表"""
        return self.ai_config.get_enabled_providers()

    def get_available_models(self, provider: str) -> List[str]:
        """获取指定提供商的可用模型"""
        return self.ai_config.get_available_models(provider)

    def clear_chat_history(self, group_name: str):
        """清除指定群的聊天历史"""
        if group_name in self.chat_histories:
            system_prompt = self.ai_config.settings.system_prompt
            self.chat_histories[group_name] = [
                ChatMessage(role="system", content=system_prompt, timestamp=time.time())
            ]

    def clear_all_histories(self):
        """清除所有聊天历史"""
        self.chat_histories.clear()

    def get_config_manager(self):
        """获取AI配置管理器"""
        return self.ai_config

    async def close(self):
        """关闭所有连接"""
        await self.client_manager.close_all()

# 为了向后兼容，保留旧的AIManager类
class AIManager(ModernAIManager):
    """向后兼容的AI管理器"""

    def __init__(self, config_manager):
        super().__init__(config_manager)
        # 保持旧接口的兼容性
        self.config = config_manager

    def update_chat_history(self, group_name: str, role: str, content: str):
        """兼容旧接口的更新聊天历史方法"""
        self.add_message(group_name, role, content)

    def get_chat_history(self, group_name: str) -> list:
        """兼容旧接口的获取聊天历史方法"""
        history = super().get_chat_history(group_name)
        # 转换为旧格式
        return [{"role": msg.role, "content": msg.content} for msg in history]