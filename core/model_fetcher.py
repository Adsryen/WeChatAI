"""
模型获取器 - 用于从API获取可用模型列表
"""
import asyncio
import aiohttp
import json
from typing import List, Optional
from .ai_types import AIProviderConfig

class ModelFetcher:
    """模型获取器"""
    
    @staticmethod
    async def fetch_models_from_api(api_key: str, base_url: str, timeout: int = 10) -> List[str]:
        """从API获取模型列表"""
        if not api_key or not base_url:
            return []
        
        # 确保URL以/v1结尾
        if not base_url.endswith('/v1'):
            if base_url.endswith('/'):
                base_url = base_url + 'v1'
            else:
                base_url = base_url + '/v1'
        
        models_url = f"{base_url}/models"
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.get(models_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'data' in data and isinstance(data['data'], list):
                            models = []
                            for model in data['data']:
                                if isinstance(model, dict) and 'id' in model:
                                    models.append(model['id'])
                            return sorted(models)
                    else:
                        print(f"获取模型列表失败，状态码: {response.status}")
                        return []
        except asyncio.TimeoutError:
            print("获取模型列表超时")
            return []
        except Exception as e:
            print(f"获取模型列表出错: {e}")
            return []
    
    @staticmethod
    def fetch_models_sync(api_key: str, base_url: str, timeout: int = 10) -> List[str]:
        """同步获取模型列表"""
        try:
            # 创建新的事件循环或使用现有的
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # 如果事件循环正在运行，使用线程池
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(
                            lambda: asyncio.run(
                                ModelFetcher.fetch_models_from_api(api_key, base_url, timeout)
                            )
                        )
                        return future.result(timeout=timeout + 5)
                else:
                    return loop.run_until_complete(
                        ModelFetcher.fetch_models_from_api(api_key, base_url, timeout)
                    )
            except RuntimeError:
                # 没有事件循环，创建新的
                return asyncio.run(
                    ModelFetcher.fetch_models_from_api(api_key, base_url, timeout)
                )
        except Exception as e:
            print(f"同步获取模型列表失败: {e}")
            return []
    
    @staticmethod
    def get_default_models(service_type: str = "openai") -> List[str]:
        """获取默认模型列表"""
        default_models = {
            "openai": [
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo",
                "gpt-4o",
                "gpt-4o-mini"
            ],
            "deepseek": [
                "deepseek-chat",
                "deepseek-coder"
            ],
            "qianwen": [
                "qwen-turbo",
                "qwen-plus",
                "qwen-max",
                "qwen-long"
            ],
            "gemini": [
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-pro"
            ],
            "claude": [
                "claude-3-haiku-20240307",
                "claude-3-sonnet-20240229",
                "claude-3-opus-20240229",
                "claude-3-5-sonnet-20241022"
            ]
        }
        return default_models.get(service_type, default_models["openai"])
    
    @staticmethod
    def detect_service_type(base_url: str) -> str:
        """根据URL检测服务类型"""
        url_lower = base_url.lower()
        
        if "deepseek" in url_lower:
            return "deepseek"
        elif "dashscope.aliyuncs.com" in url_lower:
            return "qianwen"
        elif "generativelanguage.googleapis.com" in url_lower:
            return "gemini"
        elif "api.openai.com" in url_lower:
            return "openai"
        elif "claude" in url_lower or "anthropic" in url_lower:
            return "claude"
        else:
            return "openai"  # 默认为OpenAI兼容
    
    @staticmethod
    def get_models_with_fallback(api_key: str, base_url: str, timeout: int = 10) -> List[str]:
        """获取模型列表，失败时返回默认列表"""
        if not api_key or not base_url:
            service_type = ModelFetcher.detect_service_type(base_url) if base_url else "openai"
            return ModelFetcher.get_default_models(service_type)
        
        # 尝试从API获取
        models = ModelFetcher.fetch_models_sync(api_key, base_url, timeout)
        
        if models:
            return models
        else:
            # 失败时返回默认模型
            service_type = ModelFetcher.detect_service_type(base_url)
            default_models = ModelFetcher.get_default_models(service_type)
            print(f"使用默认模型列表: {service_type}")
            return default_models

class ModelCache:
    """模型缓存"""
    
    def __init__(self):
        self._cache = {}
        self._cache_timeout = 300  # 5分钟缓存
    
    def get_cache_key(self, api_key: str, base_url: str) -> str:
        """生成缓存键"""
        # 使用API key的前8位和base_url作为缓存键
        key_prefix = api_key[:8] if len(api_key) >= 8 else api_key
        return f"{key_prefix}_{base_url}"
    
    def get_cached_models(self, api_key: str, base_url: str) -> Optional[List[str]]:
        """获取缓存的模型列表"""
        cache_key = self.get_cache_key(api_key, base_url)
        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            import time
            if time.time() - cached_data['timestamp'] < self._cache_timeout:
                return cached_data['models']
        return None
    
    def cache_models(self, api_key: str, base_url: str, models: List[str]):
        """缓存模型列表"""
        cache_key = self.get_cache_key(api_key, base_url)
        import time
        self._cache[cache_key] = {
            'models': models,
            'timestamp': time.time()
        }
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()

# 全局模型缓存实例
model_cache = ModelCache()
