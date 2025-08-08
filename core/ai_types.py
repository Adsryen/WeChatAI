"""
AI功能相关的类型定义
"""
from typing import Dict, List, Optional, Union, Literal
from dataclasses import dataclass, field
from enum import Enum

class AIProvider(Enum):
    """AI提供商枚举"""
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"
    QIANWEN = "qianwen"
    OPENAI = "openai"
    NEWAPI = "newapi"

@dataclass
class AIModel:
    """AI模型信息"""
    id: str
    name: str
    provider: AIProvider
    description: Optional[str] = None
    max_tokens: int = 4000
    supports_stream: bool = True
    cost_per_1k_tokens: float = 0.0
    available: bool = True

@dataclass
class ChatMessage:
    """聊天消息"""
    role: Literal["system", "user", "assistant"]
    content: str
    timestamp: Optional[float] = None
    tokens: Optional[int] = None

@dataclass
class AIProviderConfig:
    """AI提供商配置"""
    enabled: bool = False
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30
    proxy: Optional[Dict[str, str]] = None
    custom_headers: Optional[Dict[str, str]] = None

@dataclass
class AISettings:
    """AI设置"""
    enabled: bool = True
    default_provider: AIProvider = AIProvider.DEEPSEEK
    stream_enabled: bool = True
    system_prompt: str = "你是AI助手，名字叫VictorAI"
    max_history_length: int = 10
    auto_clear_history: bool = False
    providers: Dict[str, AIProviderConfig] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化默认提供商配置"""
        if not self.providers:
            self.providers = {
                "deepseek": AIProviderConfig(
                    enabled=True,
                    base_url="https://api.deepseek.com/v1",
                    model="deepseek-chat",
                    temperature=0.7,
                    max_tokens=2000
                ),
                "gemini": AIProviderConfig(
                    enabled=False,
                    base_url="https://generativelanguage.googleapis.com/v1beta",
                    model="gemini-1.5-flash",
                    temperature=0.7,
                    max_tokens=2000
                ),
                "qianwen": AIProviderConfig(
                    enabled=False,
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    model="qwen-turbo",
                    temperature=0.7,
                    max_tokens=2000
                ),
                "openai": AIProviderConfig(
                    enabled=False,
                    base_url="https://api.openai.com/v1",
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=2000
                ),
                "newapi": AIProviderConfig(
                    enabled=False,
                    base_url="",
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=2000
                )
            }

@dataclass
class ChatCompletionRequest:
    """聊天完成请求"""
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 2000
    stream: bool = False
    system: Optional[str] = None

@dataclass
class ChatCompletionResponse:
    """聊天完成响应"""
    id: str
    model: str
    choices: List[Dict]
    usage: Optional[Dict] = None
    created: Optional[int] = None

@dataclass
class ConnectionTestResult:
    """连接测试结果"""
    success: bool
    response_time: Optional[float] = None
    error: Optional[str] = None
    model_count: Optional[int] = None

# 预设提示词模板
AI_PROMPTS = {
    "friendly": "你是一个友善、耐心的AI助手，名字叫VictorAI。你总是以积极的态度回答问题，用简洁明了的语言帮助用户解决问题。",
    "professional": "你是一个专业的AI助手，名字叫VictorAI。你具备丰富的知识和经验，能够提供准确、详细的信息和建议。回答问题时保持客观、严谨的态度。",
    "creative": "你是一个富有创意的AI助手，名字叫VictorAI。你善于从不同角度思考问题，能够提供创新的想法和解决方案。你的回答充满想象力和启发性。",
    "technical": "你是一个技术专家AI助手，名字叫VictorAI。你精通编程、系统架构和技术问题解决。你能提供准确的技术建议和代码示例。",
    "translator": "你是一个专业的翻译助手，名字叫VictorAI。你能准确地在中文和其他语言之间进行翻译，保持原文的语义和语调。"
}

# 模型推荐配置
MODEL_RECOMMENDATIONS = {
    "chat": ["deepseek-chat", "gpt-3.5-turbo", "gemini-1.5-flash"],
    "code": ["deepseek-coder", "gpt-4", "claude-3-sonnet"],
    "creative": ["gpt-4", "claude-3-opus", "gemini-1.5-pro"],
    "analysis": ["gpt-4", "claude-3-sonnet", "qwen-max"]
}
