from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QComboBox,
                             QTabWidget, QWidget, QListWidget, QInputDialog,
                             QCheckBox, QGridLayout, QFrame, QScrollArea,
                             QGroupBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QMessageBox
from core.ai_config import AIConfigManager
from core.ai_types import AIProvider
from core.model_fetcher import ModelFetcher, model_cache

class ModelFetchThread(QThread):
    """模型获取线程"""
    models_fetched = Signal(list)
    fetch_failed = Signal(str)

    def __init__(self, api_key, base_url):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url

    def run(self):
        try:
            # 先检查缓存
            cached_models = model_cache.get_cached_models(self.api_key, self.base_url)
            if cached_models:
                self.models_fetched.emit(cached_models)
                return

            # 从API获取
            models = ModelFetcher.get_models_with_fallback(self.api_key, self.base_url)
            if models:
                # 缓存结果
                model_cache.cache_models(self.api_key, self.base_url, models)
                self.models_fetched.emit(models)
            else:
                self.fetch_failed.emit("无法获取模型列表")
        except Exception as e:
            self.fetch_failed.emit(str(e))

class ModernButton(QPushButton):
    """现代化按钮组件"""
    def __init__(self, text='', button_type='primary', parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setMinimumHeight(36)
        self.setFont(QFont('SF Pro Display', 13))
        self.update_style()

    def update_style(self):
        if self.button_type == 'primary':
            self.setStyleSheet("""
                QPushButton {
                    background-color: #007AFF;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #0069D9;
                }
                QPushButton:pressed {
                    background-color: #0051A8;
                }
            """)
        elif self.button_type == 'secondary':
            self.setStyleSheet("""
                QPushButton {
                    background-color: #F2F2F7;
                    color: #1D1D1F;
                    border: 1px solid #D2D2D7;
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #E5E5EA;
                    border-color: #C7C7CC;
                }
                QPushButton:pressed {
                    background-color: #D1D1D6;
                }
            """)

class ModernLineEdit(QLineEdit):
    """现代化输入框组件"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #E5E5EA;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                selection-background-color: #007AFF;
            }
            QLineEdit:focus {
                border-color: #007AFF;
                background-color: #FAFBFF;
            }
            QLineEdit:hover {
                border-color: #C7C7CC;
            }
        """)

class ModernComboBox(QComboBox):
    """现代化下拉框组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #E5E5EA;
                border-radius: 8px;
                padding: 8px 12px;
                min-height: 20px;
                font-size: 14px;
            }
            QComboBox:focus {
                border-color: #007AFF;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #86868B;
                margin-right: 5px;
            }
        """)

class ModernTextEdit(QTextEdit):
    """现代化文本编辑框组件"""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #E5E5EA;
                border-radius: 8px;
                padding: 10px 12px;
                font-size: 14px;
                selection-background-color: #007AFF;
            }
            QTextEdit:focus {
                border-color: #007AFF;
                background-color: #FAFBFF;
            }
            QTextEdit:hover {
                border-color: #C7C7CC;
            }
        """)

class SettingsDialog(QDialog):
    def __init__(self, config_manager, chat_manager, parent=None):
        super().__init__(parent)
        self.config = config_manager
        self.chat = chat_manager
        # 初始化AI配置管理器
        self.ai_config = AIConfigManager()
        self.setup_ui()
        self.load_settings()
        self.apply_modern_style()

    def apply_modern_style(self):
        """应用现代化样式"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FAFAFA, stop:1 #F0F0F0);
                border-radius: 12px;
            }
            QWidget {
                font-family: 'SF Pro Display', 'Microsoft YaHei UI', sans-serif;
            }
            QLabel {
                color: #1D1D1F;
                font-size: 14px;
            }
            QLabel[class="section-title"] {
                color: #1D1D1F;
                font-size: 16px;
                font-weight: 600;
                margin: 8px 0px;
            }
            QLabel[class="description"] {
                color: #86868B;
                font-size: 12px;
                margin-bottom: 8px;
            }
            QTabWidget::pane {
                border: none;
                background-color: transparent;
                margin-top: 10px;
            }
            QTabBar::tab {
                background-color: transparent;
                border: none;
                padding: 12px 20px;
                margin-right: 4px;
                border-radius: 8px;
                color: #86868B;
                font-size: 14px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #007AFF;
                border: 2px solid #007AFF;
            }
            QTabBar::tab:hover:!selected {
                background-color: #F2F2F7;
                color: #1D1D1F;
            }
            QCheckBox {
                color: #1D1D1F;
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #D2D2D7;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #007AFF;
                border-color: #007AFF;
            }
            QCheckBox::indicator:hover {
                border-color: #007AFF;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #1D1D1F;
                border: 2px solid #E5E5EA;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                background-color: white;
            }
        """)

    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("设置")
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.resize(480, 600)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # 标题
        title_label = QLabel("应用设置")
        title_label.setFont(QFont('SF Pro Display', 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #1D1D1F; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # 创建标签页
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # API设置页
        api_tab = self.create_api_tab()
        tab_widget.addTab(api_tab, "🤖 模型设置")

        # 网络代理设置页
        proxy_tab = self.create_proxy_tab()
        tab_widget.addTab(proxy_tab, "🌐 网络代理")

        # 系统提示词设置页
        prompt_tab = self.create_prompt_tab()
        tab_widget.addTab(prompt_tab, "💬 提示词设置")

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        # 添加弹性空间
        button_layout.addStretch()

        cancel_btn = ModernButton("取消", "secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = ModernButton("保存设置", "primary")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)

        main_layout.addLayout(button_layout)

    def create_api_tab(self):
        """创建API设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)

        # 标题和描述
        title_label = QLabel("AI模型配置")
        title_label.setProperty("class", "section-title")
        layout.addWidget(title_label)

        desc_label = QLabel("配置AI服务的API接口和模型选择")
        desc_label.setProperty("class", "description")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # NewAPI配置组
        newapi_group = QGroupBox("AI服务配置")
        newapi_layout = QVBoxLayout(newapi_group)
        newapi_layout.setSpacing(12)

        # API服务说明
        service_desc = QLabel("支持OpenAI兼容的API服务，如DeepSeek、通义千问、ChatGPT等")
        service_desc.setProperty("class", "description")
        service_desc.setWordWrap(True)
        newapi_layout.addWidget(service_desc)

        # API Key配置
        key_layout = QVBoxLayout()
        key_layout.setSpacing(6)
        key_layout.addWidget(QLabel("API Key:"))
        self.newapi_key = ModernLineEdit("请输入您的API Key")
        key_layout.addWidget(self.newapi_key)
        newapi_layout.addLayout(key_layout)

        # Base URL配置
        url_layout = QVBoxLayout()
        url_layout.setSpacing(6)
        url_layout.addWidget(QLabel("API Base URL:"))
        self.newapi_url = ModernLineEdit("https://api.deepseek.com/v1")
        url_layout.addWidget(self.newapi_url)

        # 常用服务快速设置
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("快速设置:"))

        deepseek_btn = ModernButton("DeepSeek", "secondary")
        deepseek_btn.clicked.connect(lambda: self._set_quick_service("deepseek"))
        quick_layout.addWidget(deepseek_btn)

        qianwen_btn = ModernButton("通义千问", "secondary")
        qianwen_btn.clicked.connect(lambda: self._set_quick_service("qianwen"))
        quick_layout.addWidget(qianwen_btn)

        openai_btn = ModernButton("OpenAI", "secondary")
        openai_btn.clicked.connect(lambda: self._set_quick_service("openai"))
        quick_layout.addWidget(openai_btn)

        quick_layout.addStretch()
        url_layout.addLayout(quick_layout)
        newapi_layout.addLayout(url_layout)

        # 模型选择
        model_layout = QVBoxLayout()
        model_layout.setSpacing(6)

        model_header_layout = QHBoxLayout()
        model_header_layout.addWidget(QLabel("选择模型:"))
        model_header_layout.addStretch()

        # 刷新模型列表按钮
        self.refresh_models_btn = ModernButton("🔄 刷新", "secondary")
        self.refresh_models_btn.setMaximumWidth(80)
        self.refresh_models_btn.clicked.connect(self._refresh_models)
        model_header_layout.addWidget(self.refresh_models_btn)

        model_layout.addLayout(model_header_layout)

        self.model_combo = ModernComboBox()
        self.model_combo.setEditable(True)  # 允许手动输入模型名称
        model_layout.addWidget(self.model_combo)

        # 模型状态标签
        self.model_status_label = QLabel("点击刷新按钮获取最新模型列表")
        self.model_status_label.setProperty("class", "description")
        model_layout.addWidget(self.model_status_label)

        # 常用模型快速选择
        model_quick_layout = QHBoxLayout()
        model_quick_layout.addWidget(QLabel("常用模型:"))

        gpt35_btn = ModernButton("GPT-3.5", "secondary")
        gpt35_btn.clicked.connect(lambda: self.model_combo.setCurrentText("gpt-3.5-turbo"))
        model_quick_layout.addWidget(gpt35_btn)

        gpt4_btn = ModernButton("GPT-4", "secondary")
        gpt4_btn.clicked.connect(lambda: self.model_combo.setCurrentText("gpt-4"))
        model_quick_layout.addWidget(gpt4_btn)

        deepseek_model_btn = ModernButton("DeepSeek", "secondary")
        deepseek_model_btn.clicked.connect(lambda: self.model_combo.setCurrentText("deepseek-chat"))
        model_quick_layout.addWidget(deepseek_model_btn)

        model_quick_layout.addStretch()
        model_layout.addLayout(model_quick_layout)
        newapi_layout.addLayout(model_layout)

        layout.addWidget(newapi_group)

        # 高级设置
        advanced_group = QGroupBox("高级设置")
        advanced_layout = QVBoxLayout(advanced_group)
        advanced_layout.setSpacing(8)

        # 温度参数
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("温度参数:"))
        self.temperature_input = ModernLineEdit("0.7")
        self.temperature_input.setMaximumWidth(100)
        temp_layout.addWidget(self.temperature_input)
        temp_layout.addWidget(QLabel("(0.1-2.0, 控制回复的随机性)"))
        temp_layout.addStretch()
        advanced_layout.addLayout(temp_layout)

        # 最大Token数
        token_layout = QHBoxLayout()
        token_layout.addWidget(QLabel("最大Token数:"))
        self.max_tokens_input = ModernLineEdit("2000")
        self.max_tokens_input.setMaximumWidth(100)
        token_layout.addWidget(self.max_tokens_input)
        token_layout.addWidget(QLabel("(控制回复的最大长度)"))
        token_layout.addStretch()
        advanced_layout.addLayout(token_layout)

        layout.addWidget(advanced_group)

        # 连接测试按钮
        test_layout = QHBoxLayout()
        test_layout.addStretch()
        self.test_btn = ModernButton("测试连接", "secondary")
        self.test_btn.clicked.connect(self._test_connection)
        test_layout.addWidget(self.test_btn)
        layout.addLayout(test_layout)

        # 添加弹性空间
        layout.addStretch()

        return tab

    def create_proxy_tab(self):
        """创建网络代理设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)

        # 标题和描述
        title_label = QLabel("网络代理设置")
        title_label.setProperty("class", "section-title")
        layout.addWidget(title_label)

        desc_label = QLabel("配置网络代理以访问被限制的AI服务（如OpenAI、Gemini等）")
        desc_label.setProperty("class", "description")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # 代理配置组
        proxy_group = QGroupBox("代理配置")
        proxy_layout = QVBoxLayout(proxy_group)
        proxy_layout.setSpacing(12)

        # 启用代理开关
        self.proxy_enabled_check = QCheckBox("启用网络代理")
        self.proxy_enabled_check.stateChanged.connect(self._on_proxy_enabled_changed)
        proxy_layout.addWidget(self.proxy_enabled_check)

        # 代理设置容器
        self.proxy_settings_widget = QWidget()
        proxy_settings_layout = QVBoxLayout(self.proxy_settings_widget)
        proxy_settings_layout.setContentsMargins(20, 0, 0, 0)
        proxy_settings_layout.setSpacing(12)

        # HTTP代理设置
        http_layout = QVBoxLayout()
        http_layout.setSpacing(6)
        http_layout.addWidget(QLabel("HTTP 代理:"))
        self.http_proxy = ModernLineEdit("http://127.0.0.1:7890")
        http_layout.addWidget(self.http_proxy)
        proxy_settings_layout.addLayout(http_layout)

        # HTTPS代理设置
        https_layout = QVBoxLayout()
        https_layout.setSpacing(6)
        https_layout.addWidget(QLabel("HTTPS 代理:"))
        self.https_proxy = ModernLineEdit("http://127.0.0.1:7890")
        https_layout.addWidget(self.https_proxy)
        proxy_settings_layout.addLayout(https_layout)

        # 快速设置按钮
        quick_proxy_layout = QHBoxLayout()
        quick_proxy_layout.addWidget(QLabel("常用代理:"))

        clash_btn = ModernButton("Clash (7890)", "secondary")
        clash_btn.clicked.connect(lambda: self._set_quick_proxy("7890"))
        quick_proxy_layout.addWidget(clash_btn)

        v2ray_btn = ModernButton("V2Ray (1080)", "secondary")
        v2ray_btn.clicked.connect(lambda: self._set_quick_proxy("1080"))
        quick_proxy_layout.addWidget(v2ray_btn)

        shadowsocks_btn = ModernButton("SS (1080)", "secondary")
        shadowsocks_btn.clicked.connect(lambda: self._set_quick_proxy("1080"))
        quick_proxy_layout.addWidget(shadowsocks_btn)

        quick_proxy_layout.addStretch()
        proxy_settings_layout.addLayout(quick_proxy_layout)

        proxy_layout.addWidget(self.proxy_settings_widget)
        layout.addWidget(proxy_group)

        # 代理测试组
        test_group = QGroupBox("连接测试")
        test_layout = QVBoxLayout(test_group)
        test_layout.setSpacing(8)

        test_desc = QLabel("测试代理连接是否正常工作")
        test_desc.setProperty("class", "description")
        test_layout.addWidget(test_desc)

        test_btn_layout = QHBoxLayout()
        test_btn_layout.addStretch()
        self.proxy_test_btn = ModernButton("测试代理连接", "secondary")
        self.proxy_test_btn.clicked.connect(self._test_proxy_connection)
        test_btn_layout.addWidget(self.proxy_test_btn)
        test_layout.addLayout(test_btn_layout)

        layout.addWidget(test_group)

        # 使用说明
        help_group = QGroupBox("使用说明")
        help_layout = QVBoxLayout(help_group)

        help_text = QLabel("""
• 代理主要用于访问被限制的AI服务（如OpenAI、Gemini）
• 常见代理软件端口：Clash (7890)、V2Ray (1080)、Shadowsocks (1080)
• 代理格式：http://127.0.0.1:端口号
• 如果不需要代理，请取消勾选"启用网络代理"
• 建议先测试代理连接再保存设置
        """.strip())
        help_text.setProperty("class", "description")
        help_text.setWordWrap(True)
        help_layout.addWidget(help_text)

        layout.addWidget(help_group)

        # 添加弹性空间
        layout.addStretch()

        return tab

    def create_prompt_tab(self):
        """创建提示词设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # 标题和描述
        title_label = QLabel("系统提示词")
        title_label.setProperty("class", "section-title")
        layout.addWidget(title_label)

        desc_label = QLabel("设置AI助手的角色和行为规范，这将影响AI的回复风格和内容")
        desc_label.setProperty("class", "description")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # 提示词输入框
        self.system_prompt = ModernTextEdit("请输入系统提示词，例如：你是一个友善的AI助手...")
        self.system_prompt.setMinimumHeight(300)
        layout.addWidget(self.system_prompt)

        # 预设提示词按钮
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("快速预设:"))

        friendly_btn = ModernButton("友善助手", "secondary")
        friendly_btn.clicked.connect(lambda: self.set_preset_prompt("friendly"))
        preset_layout.addWidget(friendly_btn)

        professional_btn = ModernButton("专业助手", "secondary")
        professional_btn.clicked.connect(lambda: self.set_preset_prompt("professional"))
        preset_layout.addWidget(professional_btn)

        creative_btn = ModernButton("创意助手", "secondary")
        creative_btn.clicked.connect(lambda: self.set_preset_prompt("creative"))
        preset_layout.addWidget(creative_btn)

        preset_layout.addStretch()
        layout.addLayout(preset_layout)

        return tab

    def set_preset_prompt(self, preset_type):
        """设置预设提示词"""
        presets = self.ai_config.get_preset_prompts()
        if preset_type in presets:
            self.system_prompt.setText(presets[preset_type])

    def _set_quick_service(self, service):
        """设置快速服务配置"""
        service_configs = {
            "deepseek": {
                "url": "https://api.deepseek.com/v1",
                "models": ["deepseek-chat", "deepseek-coder"]
            },
            "qianwen": {
                "url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                "models": ["qwen-turbo", "qwen-plus", "qwen-max"]
            },
            "openai": {
                "url": "https://api.openai.com/v1",
                "models": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]
            }
        }

        if service in service_configs:
            config = service_configs[service]
            self.newapi_url.setText(config["url"])

            # 先使用默认模型列表
            self.model_combo.clear()
            self.model_combo.addItems(config["models"])
            if config["models"]:
                self.model_combo.setCurrentText(config["models"][0])

            self.model_status_label.setText("已设置默认模型，建议点击刷新获取最新列表")

            # 如果有API Key，自动刷新模型列表
            if self.newapi_key.text().strip():
                QTimer.singleShot(500, self._refresh_models)  # 延迟500ms后自动刷新

    def _test_connection(self):
        """测试API连接"""
        if not self.newapi_key.text().strip():
            QMessageBox.warning(self, "测试失败", "请先输入API Key")
            return

        if not self.newapi_url.text().strip():
            QMessageBox.warning(self, "测试失败", "请先输入API Base URL")
            return

        self.test_btn.setText("测试中...")
        self.test_btn.setEnabled(False)

        # 这里可以添加实际的连接测试逻辑
        # 暂时显示一个简单的消息
        QTimer.singleShot(1000, lambda: self._show_test_result())

    def _show_test_result(self):
        """显示测试结果"""
        self.test_btn.setText("测试连接")
        self.test_btn.setEnabled(True)
        QMessageBox.information(self, "连接测试", "连接测试功能正在开发中...")

    def _on_proxy_enabled_changed(self, state):
        """处理代理启用状态变化"""
        enabled = bool(state)
        self.proxy_settings_widget.setEnabled(enabled)
        if not enabled:
            self.http_proxy.clear()
            self.https_proxy.clear()

    def _set_quick_proxy(self, port):
        """设置快速代理配置"""
        proxy_url = f"http://127.0.0.1:{port}"
        self.http_proxy.setText(proxy_url)
        self.https_proxy.setText(proxy_url)

    def _test_proxy_connection(self):
        """测试代理连接"""
        if not self.proxy_enabled_check.isChecked():
            QMessageBox.warning(self, "测试失败", "请先启用网络代理")
            return

        if not self.http_proxy.text().strip():
            QMessageBox.warning(self, "测试失败", "请先配置代理地址")
            return

        self.proxy_test_btn.setText("测试中...")
        self.proxy_test_btn.setEnabled(False)

        # 这里可以添加实际的代理测试逻辑
        QTimer.singleShot(1000, lambda: self._show_proxy_test_result())

    def _show_proxy_test_result(self):
        """显示代理测试结果"""
        self.proxy_test_btn.setText("测试代理连接")
        self.proxy_test_btn.setEnabled(True)
        QMessageBox.information(self, "代理测试", "代理连接测试功能正在开发中...")

    def _refresh_models(self):
        """刷新模型列表"""
        api_key = self.newapi_key.text().strip()
        base_url = self.newapi_url.text().strip()

        if not api_key:
            QMessageBox.warning(self, "刷新失败", "请先输入API Key")
            return

        if not base_url:
            QMessageBox.warning(self, "刷新失败", "请先输入API Base URL")
            return

        # 禁用刷新按钮并显示加载状态
        self.refresh_models_btn.setText("刷新中...")
        self.refresh_models_btn.setEnabled(False)
        self.model_status_label.setText("正在获取模型列表...")

        # 创建并启动模型获取线程
        self.model_fetch_thread = ModelFetchThread(api_key, base_url)
        self.model_fetch_thread.models_fetched.connect(self._on_models_fetched)
        self.model_fetch_thread.fetch_failed.connect(self._on_models_fetch_failed)
        self.model_fetch_thread.start()

    def _on_models_fetched(self, models):
        """模型获取成功"""
        self.refresh_models_btn.setText("🔄 刷新")
        self.refresh_models_btn.setEnabled(True)

        if models:
            # 保存当前选中的模型
            current_model = self.model_combo.currentText()

            # 更新模型列表
            self.model_combo.clear()
            self.model_combo.addItems(models)

            # 恢复之前选中的模型（如果存在）
            if current_model and current_model in models:
                self.model_combo.setCurrentText(current_model)
            elif models:
                self.model_combo.setCurrentText(models[0])

            self.model_status_label.setText(f"已获取 {len(models)} 个模型")
        else:
            self.model_status_label.setText("未获取到模型列表")

    def _on_models_fetch_failed(self, error):
        """模型获取失败"""
        self.refresh_models_btn.setText("🔄 刷新")
        self.refresh_models_btn.setEnabled(True)
        self.model_status_label.setText(f"获取失败: {error}")

        # 使用默认模型列表
        service_type = ModelFetcher.detect_service_type(self.newapi_url.text().strip())
        default_models = ModelFetcher.get_default_models(service_type)

        current_model = self.model_combo.currentText()
        self.model_combo.clear()
        self.model_combo.addItems(default_models)

        if current_model and current_model in default_models:
            self.model_combo.setCurrentText(current_model)
        elif default_models:
            self.model_combo.setCurrentText(default_models[0])

    def load_settings(self):
        """加载设置"""
        # 加载AI配置
        self.ai_config.load_config()

        # NewAPI设置
        self.newapi_key.setText(self.ai_config.get_api_key("newapi"))

        newapi_config = self.ai_config.get_provider_config("newapi")
        if newapi_config:
            self.newapi_url.setText(newapi_config.base_url or "https://api.deepseek.com/v1")
            self.temperature_input.setText(str(newapi_config.temperature))
            self.max_tokens_input.setText(str(newapi_config.max_tokens))

            # 初始化模型列表
            base_url = newapi_config.base_url or "https://api.deepseek.com/v1"
            service_type = ModelFetcher.detect_service_type(base_url)
            default_models = ModelFetcher.get_default_models(service_type)

            self.model_combo.clear()
            self.model_combo.addItems(default_models)

            # 设置当前模型
            current_model = newapi_config.model or "deepseek-chat"
            if current_model in default_models:
                self.model_combo.setCurrentText(current_model)
            elif default_models:
                self.model_combo.setCurrentText(default_models[0])

            self.model_status_label.setText("已加载默认模型列表，点击刷新获取最新列表")

        # 代理设置
        proxy = self.config.get_proxy()
        proxy_enabled = bool(proxy.get("http") or proxy.get("https"))
        self.proxy_enabled_check.setChecked(proxy_enabled)
        self.http_proxy.setText(proxy.get("http", ""))
        self.https_proxy.setText(proxy.get("https", ""))

        # 启用/禁用代理设置
        self.proxy_settings_widget.setEnabled(proxy_enabled)

        # 系统提示词
        self.system_prompt.setText(self.ai_config.settings.system_prompt)

        # 连接代理复选框信号
        self.proxy_enabled_check.stateChanged.connect(self._on_proxy_enabled_changed)

    def save_settings(self):
        """保存设置"""
        try:
            # 保存NewAPI配置
            self.ai_config.set_api_key("newapi", self.newapi_key.text().strip())

            newapi_config = self.ai_config.get_provider_config("newapi")
            if newapi_config:
                newapi_config.base_url = self.newapi_url.text().strip()
                newapi_config.model = self.model_combo.currentText().strip()
                newapi_config.enabled = True

                # 保存高级设置
                try:
                    newapi_config.temperature = float(self.temperature_input.text())
                except ValueError:
                    newapi_config.temperature = 0.7

                try:
                    newapi_config.max_tokens = int(self.max_tokens_input.text())
                except ValueError:
                    newapi_config.max_tokens = 2000

                self.ai_config.set_provider_config("newapi", newapi_config)

            # 设置NewAPI为默认提供商
            self.ai_config.settings.default_provider = AIProvider.NEWAPI

            # 保存系统提示词
            self.ai_config.settings.system_prompt = self.system_prompt.toPlainText().strip()

            # 保存AI配置
            self.ai_config.save_config()

            # 向后兼容：保存到旧配置系统
            self.config.set_api_key("newapi", self.newapi_key.text().strip())

            # 代理设置
            if self.proxy_enabled_check.isChecked():
                self.config.set_proxy(self.http_proxy.text().strip(), self.https_proxy.text().strip())
            else:
                self.config.set_proxy("", "")

            # 默认模型
            self.config.config["default_model"] = "newapi"
            self.config.save_config()

            # 系统提示词
            self.config.set_system_prompt(self.system_prompt.toPlainText().strip())

            # 显示保存成功的反馈
            self.show_save_feedback()

            # 延迟关闭对话框
            QTimer.singleShot(800, self.accept)

        except Exception as e:
            QMessageBox.warning(self, "保存失败", f"保存设置时出现错误：{str(e)}")

    def show_save_feedback(self):
        """显示保存成功的反馈"""
        # 这里可以添加一个临时的成功提示
        pass