# 模型设置优化说明

## 概述

根据您的要求，我对WeChatAI的模型设置进行了全面优化，简化为只保留NewAPI配置和动态模型获取功能，并将网络代理设置独立为单独的标签页。

## 主要改进

### 1. 简化的模型配置

#### 移除的功能
- ❌ DeepSeek专用配置
- ❌ Gemini专用配置  
- ❌ 通义千问专用配置
- ❌ OpenAI专用配置
- ❌ 复杂的提供商选择

#### 保留的功能
- ✅ 统一的NewAPI配置
- ✅ 动态模型列表获取
- ✅ 手动模型输入
- ✅ 高级参数设置

### 2. 动态模型获取

#### 核心功能
```python
# 从 /v1/models 端点获取模型列表
GET {base_url}/v1/models
Authorization: Bearer {api_key}
```

#### 实现特性
- **自动获取**: 从API端点动态获取可用模型
- **智能缓存**: 5分钟缓存机制，避免重复请求
- **失败回退**: API失败时自动使用默认模型列表
- **服务检测**: 根据URL自动检测服务类型
- **异步处理**: 使用线程避免界面阻塞

### 3. 网络代理独立配置

#### 新的代理标签页
- 🌐 独立的"网络代理"标签页
- 🔧 简化的代理开关控制
- ⚡ 常用代理端口快速设置
- 🧪 代理连接测试功能
- 📖 详细的使用说明

## 技术实现

### 1. 模型获取器 (`core/model_fetcher.py`)

#### ModelFetcher类
```python
class ModelFetcher:
    @staticmethod
    async def fetch_models_from_api(api_key: str, base_url: str) -> List[str]:
        """从API获取模型列表"""
    
    @staticmethod
    def fetch_models_sync(api_key: str, base_url: str) -> List[str]:
        """同步获取模型列表"""
    
    @staticmethod
    def get_models_with_fallback(api_key: str, base_url: str) -> List[str]:
        """获取模型列表，失败时返回默认列表"""
```

#### 服务类型检测
```python
def detect_service_type(base_url: str) -> str:
    """根据URL检测服务类型"""
    if "deepseek" in url_lower:
        return "deepseek"
    elif "dashscope.aliyuncs.com" in url_lower:
        return "qianwen"
    elif "api.openai.com" in url_lower:
        return "openai"
    # ...
```

#### 默认模型列表
```python
default_models = {
    "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o"],
    "deepseek": ["deepseek-chat", "deepseek-coder"],
    "qianwen": ["qwen-turbo", "qwen-plus", "qwen-max"],
    "gemini": ["gemini-1.5-flash", "gemini-1.5-pro"],
    "claude": ["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"]
}
```

### 2. 异步模型获取 (`ui/settings_dialog.py`)

#### ModelFetchThread类
```python
class ModelFetchThread(QThread):
    models_fetched = Signal(list)
    fetch_failed = Signal(str)
    
    def run(self):
        # 检查缓存
        cached_models = model_cache.get_cached_models(self.api_key, self.base_url)
        if cached_models:
            self.models_fetched.emit(cached_models)
            return
        
        # 从API获取
        models = ModelFetcher.get_models_with_fallback(self.api_key, self.base_url)
        if models:
            model_cache.cache_models(self.api_key, self.base_url, models)
            self.models_fetched.emit(models)
```

### 3. 智能缓存机制

#### ModelCache类
```python
class ModelCache:
    def __init__(self):
        self._cache = {}
        self._cache_timeout = 300  # 5分钟
    
    def get_cached_models(self, api_key: str, base_url: str) -> Optional[List[str]]:
        """获取缓存的模型列表"""
    
    def cache_models(self, api_key: str, base_url: str, models: List[str]):
        """缓存模型列表"""
```

## 用户界面优化

### 1. 模型设置标签页

#### 布局结构
```
🤖 模型设置
├── AI服务配置
│   ├── API Key 输入
│   ├── Base URL 输入
│   ├── 快速设置按钮 (DeepSeek/通义千问/OpenAI)
│   └── 模型选择
│       ├── 模型下拉框 (可编辑)
│       ├── 🔄 刷新按钮
│       ├── 状态标签
│       └── 常用模型快速选择
├── 高级设置
│   ├── 温度参数 (0.1-2.0)
│   └── 最大Token数
└── 🧪 测试连接
```

#### 交互流程
1. **输入配置**: 用户输入API Key和Base URL
2. **快速设置**: 点击服务按钮自动填入URL
3. **刷新模型**: 点击刷新按钮获取最新模型列表
4. **选择模型**: 从下拉框选择或手动输入模型名
5. **测试连接**: 验证配置是否正确

### 2. 网络代理标签页

#### 功能特性
- **代理开关**: 一键启用/禁用代理
- **代理配置**: HTTP/HTTPS代理地址设置
- **快速设置**: Clash(7890)、V2Ray(1080)等常用端口
- **连接测试**: 验证代理是否工作正常
- **使用说明**: 详细的配置指导

## 使用指南

### 1. 基本配置步骤

1. **打开设置页面**
   - 点击主界面的"设置"按钮

2. **配置AI服务**
   - 切换到"🤖 模型设置"标签页
   - 输入您的API Key
   - 选择或输入API Base URL
   - 点击快速设置按钮（可选）

3. **获取模型列表**
   - 点击"🔄 刷新"按钮
   - 等待模型列表加载完成
   - 从下拉框选择合适的模型

4. **配置网络代理**（如需要）
   - 切换到"🌐 网络代理"标签页
   - 勾选"启用网络代理"
   - 输入代理地址或使用快速设置
   - 点击"测试代理连接"验证

5. **保存设置**
   - 点击"保存设置"按钮
   - 等待保存完成提示

### 2. 支持的服务

#### DeepSeek
- **URL**: `https://api.deepseek.com/v1`
- **模型**: deepseek-chat, deepseek-coder
- **特点**: 性价比高，中文友好

#### 通义千问
- **URL**: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **模型**: qwen-turbo, qwen-plus, qwen-max
- **特点**: 阿里云服务，国内访问稳定

#### OpenAI
- **URL**: `https://api.openai.com/v1`
- **模型**: gpt-3.5-turbo, gpt-4, gpt-4-turbo
- **特点**: 功能强大，需要代理访问

#### 自定义服务
- 支持任何OpenAI兼容的API服务
- 可以是自建服务或第三方代理

### 3. 故障排除

#### 模型获取失败
- **检查API Key**: 确保API Key正确且有效
- **检查网络**: 确认网络连接正常
- **检查代理**: 如果需要代理，确保代理配置正确
- **使用默认**: 系统会自动回退到默认模型列表

#### 连接测试失败
- **验证凭据**: 检查API Key和URL是否正确
- **网络问题**: 检查网络连接和防火墙设置
- **代理设置**: 确认代理配置是否正确

## 技术优势

### 1. 性能优化
- **异步处理**: 避免界面阻塞
- **智能缓存**: 减少重复API调用
- **失败回退**: 确保功能可用性

### 2. 用户体验
- **简化配置**: 统一的API配置界面
- **智能检测**: 自动识别服务类型
- **实时反馈**: 清晰的状态提示

### 3. 扩展性
- **服务无关**: 支持任何OpenAI兼容服务
- **模型灵活**: 支持动态模型列表和手动输入
- **配置独立**: 代理设置与模型配置分离

## 总结

本次优化实现了：
- ✅ 简化的模型配置界面
- ✅ 动态模型列表获取功能
- ✅ 独立的网络代理设置
- ✅ 智能缓存和错误处理
- ✅ 更好的用户体验

新的设置系统更加简洁、灵活，同时保持了强大的功能性和良好的用户体验。
