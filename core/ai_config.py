"""
AI配置管理器 - 基于现代化架构设计
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import asdict, fields
from dotenv import load_dotenv

from .ai_types import (
    AISettings, AIProviderConfig, AIProvider, AIModel,
    AI_PROMPTS, MODEL_RECOMMENDATIONS
)

class AIConfigManager:
    """AI配置管理器"""
    
    def __init__(self, config_file: str = "data/ai_config.json"):
        self.config_file = Path(config_file)
        self.settings: AISettings = AISettings()
        self._load_env()
        self._ensure_config_dir()
        self.load_config()
    
    def _load_env(self):
        """加载环境变量"""
        load_dotenv()
        
        # 从环境变量加载API密钥
        env_keys = {
            "deepseek": os.getenv("DEEPSEEK_API_KEY", ""),
            "gemini": os.getenv("GEMINI_API_KEY", ""),
            "qianwen": os.getenv("QIANWEN_API_KEY", ""),
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "newapi": os.getenv("NEWAPI_API_KEY", "")
        }
        
        # 更新默认配置中的API密钥
        for provider, api_key in env_keys.items():
            if api_key and provider in self.settings.providers:
                self.settings.providers[provider].api_key = api_key
    
    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._deserialize_settings(data)
                return True
            else:
                # 首次运行，保存默认配置
                self.save_config()
                return True
        except Exception as e:
            print(f"加载AI配置失败: {e}")
            return False
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            data = self._serialize_settings()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存AI配置失败: {e}")
            return False
    
    def _serialize_settings(self) -> Dict[str, Any]:
        """序列化设置为字典"""
        data = {
            "enabled": self.settings.enabled,
            "default_provider": self.settings.default_provider.value,
            "stream_enabled": self.settings.stream_enabled,
            "system_prompt": self.settings.system_prompt,
            "max_history_length": self.settings.max_history_length,
            "auto_clear_history": self.settings.auto_clear_history,
            "providers": {}
        }
        
        # 序列化提供商配置
        for name, config in self.settings.providers.items():
            data["providers"][name] = {
                "enabled": config.enabled,
                "api_key": config.api_key,
                "base_url": config.base_url,
                "model": config.model,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "timeout": config.timeout,
                "proxy": config.proxy,
                "custom_headers": config.custom_headers
            }
        
        return data
    
    def _deserialize_settings(self, data: Dict[str, Any]):
        """从字典反序列化设置"""
        self.settings.enabled = data.get("enabled", True)
        self.settings.default_provider = AIProvider(data.get("default_provider", "deepseek"))
        self.settings.stream_enabled = data.get("stream_enabled", True)
        self.settings.system_prompt = data.get("system_prompt", "你是AI助手，名字叫VictorAI")
        self.settings.max_history_length = data.get("max_history_length", 10)
        self.settings.auto_clear_history = data.get("auto_clear_history", False)
        
        # 反序列化提供商配置
        providers_data = data.get("providers", {})
        for name, config_data in providers_data.items():
            if name in self.settings.providers:
                config = self.settings.providers[name]
                config.enabled = config_data.get("enabled", False)
                config.api_key = config_data.get("api_key", "")
                config.base_url = config_data.get("base_url", "")
                config.model = config_data.get("model", "")
                config.temperature = config_data.get("temperature", 0.7)
                config.max_tokens = config_data.get("max_tokens", 2000)
                config.timeout = config_data.get("timeout", 30)
                config.proxy = config_data.get("proxy")
                config.custom_headers = config_data.get("custom_headers")
    
    # 配置访问方法
    def get_provider_config(self, provider: str) -> Optional[AIProviderConfig]:
        """获取提供商配置"""
        return self.settings.providers.get(provider)
    
    def set_provider_config(self, provider: str, config: AIProviderConfig):
        """设置提供商配置"""
        self.settings.providers[provider] = config
        self.save_config()
    
    def get_api_key(self, provider: str) -> str:
        """获取API密钥"""
        config = self.get_provider_config(provider)
        return config.api_key if config else ""
    
    def set_api_key(self, provider: str, api_key: str):
        """设置API密钥"""
        if provider in self.settings.providers:
            self.settings.providers[provider].api_key = api_key
            self.save_config()
    
    def get_enabled_providers(self) -> List[str]:
        """获取已启用的提供商列表"""
        return [name for name, config in self.settings.providers.items() if config.enabled]
    
    def get_available_models(self, provider: str) -> List[str]:
        """获取可用模型列表"""
        # 这里可以根据提供商返回支持的模型列表
        model_lists = {
            "deepseek": ["deepseek-chat", "deepseek-coder"],
            "gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
            "qianwen": ["qwen-turbo", "qwen-plus", "qwen-max"],
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            "newapi": ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet"]
        }
        return model_lists.get(provider, [])
    
    def get_recommended_models(self, task: str = "chat") -> List[str]:
        """获取推荐模型"""
        return MODEL_RECOMMENDATIONS.get(task, MODEL_RECOMMENDATIONS["chat"])
    
    def get_preset_prompts(self) -> Dict[str, str]:
        """获取预设提示词"""
        return AI_PROMPTS
    
    def test_provider_connection(self, provider: str) -> bool:
        """测试提供商连接"""
        config = self.get_provider_config(provider)
        if not config or not config.api_key:
            return False
        
        # 这里可以实现实际的连接测试
        # 暂时返回True，实际实现需要调用对应的API
        return True
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.settings = AISettings()
        self._load_env()  # 重新加载环境变量
        self.save_config()
    
    def export_config(self, file_path: str) -> bool:
        """导出配置"""
        try:
            data = self._serialize_settings()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """导入配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._deserialize_settings(data)
                self.save_config()
            return True
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False
