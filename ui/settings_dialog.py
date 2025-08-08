from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QComboBox,
                             QTabWidget, QWidget, QListWidget, QInputDialog,
                             QCheckBox, QGridLayout, QFrame, QScrollArea,
                             QGroupBox, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import QMessageBox
from core.ai_config import AIConfigManager
from core.ai_types import AIProvider

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

        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; }")

        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)

        # 默认模型选择组
        model_group = QGroupBox("默认AI提供商")
        model_layout = QVBoxLayout(model_group)
        model_layout.setSpacing(8)

        desc_label = QLabel("选择默认使用的AI提供商和模型")
        desc_label.setProperty("class", "description")
        model_layout.addWidget(desc_label)

        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("提供商:"))
        self.provider_combo = ModernComboBox()
        self.provider_combo.addItems(["deepseek", "gemini", "qianwen", "openai", "newapi"])
        self.provider_combo.currentTextChanged.connect(self._on_provider_changed)
        provider_layout.addWidget(self.provider_combo)
        model_layout.addLayout(provider_layout)

        model_select_layout = QHBoxLayout()
        model_select_layout.addWidget(QLabel("模型:"))
        self.model_combo = ModernComboBox()
        model_select_layout.addWidget(self.model_combo)
        model_layout.addLayout(model_select_layout)

        layout.addWidget(model_group)

        # DeepSeek设置组
        deepseek_group = QGroupBox("DeepSeek 配置")
        deepseek_layout = QVBoxLayout(deepseek_group)
        deepseek_layout.setSpacing(8)

        deepseek_desc = QLabel("DeepSeek是一个强大的开源大语言模型")
        deepseek_desc.setProperty("class", "description")
        deepseek_layout.addWidget(deepseek_desc)

        deepseek_layout.addWidget(QLabel("API Key:"))
        self.deepseek_key = ModernLineEdit("请输入DeepSeek API Key")
        deepseek_layout.addWidget(self.deepseek_key)

        layout.addWidget(deepseek_group)

        # Gemini设置组
        gemini_group = QGroupBox("Gemini 配置")
        gemini_layout = QVBoxLayout(gemini_group)
        gemini_layout.setSpacing(8)

        gemini_desc = QLabel("Google Gemini是Google开发的多模态AI模型")
        gemini_desc.setProperty("class", "description")
        gemini_layout.addWidget(gemini_desc)

        gemini_layout.addWidget(QLabel("API Key:"))
        self.gemini_key = ModernLineEdit("请输入Gemini API Key")
        gemini_layout.addWidget(self.gemini_key)

        # 代理设置
        self.gemini_proxy_check = QCheckBox("启用网络代理")
        gemini_layout.addWidget(self.gemini_proxy_check)

        proxy_widget = QWidget()
        proxy_layout = QGridLayout(proxy_widget)
        proxy_layout.setContentsMargins(20, 8, 0, 8)
        proxy_layout.setSpacing(8)

        proxy_layout.addWidget(QLabel("HTTP 代理:"), 0, 0)
        self.http_proxy = ModernLineEdit("http://127.0.0.1:7890")
        proxy_layout.addWidget(self.http_proxy, 0, 1)

        proxy_layout.addWidget(QLabel("HTTPS 代理:"), 1, 0)
        self.https_proxy = ModernLineEdit("http://127.0.0.1:7890")
        proxy_layout.addWidget(self.https_proxy, 1, 1)

        gemini_layout.addWidget(proxy_widget)
        layout.addWidget(gemini_group)

        # 通义千问设置组
        qianwen_group = QGroupBox("通义千问 配置")
        qianwen_layout = QVBoxLayout(qianwen_group)
        qianwen_layout.setSpacing(8)

        qianwen_desc = QLabel("阿里云通义千问大语言模型")
        qianwen_desc.setProperty("class", "description")
        qianwen_layout.addWidget(qianwen_desc)

        qianwen_layout.addWidget(QLabel("API Key:"))
        self.qianwen_key = ModernLineEdit("请输入通义千问 API Key")
        qianwen_layout.addWidget(self.qianwen_key)

        layout.addWidget(qianwen_group)

        # OpenAI设置组
        openai_group = QGroupBox("OpenAI 配置")
        openai_layout = QVBoxLayout(openai_group)
        openai_layout.setSpacing(8)

        openai_desc = QLabel("OpenAI官方API服务")
        openai_desc.setProperty("class", "description")
        openai_layout.addWidget(openai_desc)

        openai_layout.addWidget(QLabel("API Key:"))
        self.openai_key = ModernLineEdit("请输入OpenAI API Key")
        openai_layout.addWidget(self.openai_key)

        layout.addWidget(openai_group)

        # NewAPI设置组
        newapi_group = QGroupBox("New-API 配置")
        newapi_layout = QVBoxLayout(newapi_group)
        newapi_layout.setSpacing(8)

        newapi_desc = QLabel("自建或第三方兼容OpenAI的API服务")
        newapi_desc.setProperty("class", "description")
        newapi_layout.addWidget(newapi_desc)

        newapi_layout.addWidget(QLabel("API Key:"))
        self.newapi_key = ModernLineEdit("请输入New-API Key")
        newapi_layout.addWidget(self.newapi_key)

        newapi_layout.addWidget(QLabel("Base URL:"))
        self.newapi_url = ModernLineEdit("https://api.example.com/v1")
        newapi_layout.addWidget(self.newapi_url)

        layout.addWidget(newapi_group)

        # 连接测试按钮
        test_layout = QHBoxLayout()
        test_layout.addStretch()
        self.test_btn = ModernButton("测试连接", "secondary")
        self.test_btn.clicked.connect(self._test_connections)
        test_layout.addWidget(self.test_btn)
        layout.addLayout(test_layout)

        # 添加弹性空间
        layout.addStretch()

        scroll.setWidget(content_widget)

        tab_layout = QVBoxLayout(tab)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.addWidget(scroll)

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

    def _on_provider_changed(self, provider):
        """当提供商改变时更新模型列表"""
        self.model_combo.clear()
        models = self.ai_config.get_available_models(provider)
        self.model_combo.addItems(models)

        # 设置默认模型
        if models:
            config = self.ai_config.get_provider_config(provider)
            if config and config.model in models:
                index = models.index(config.model)
                self.model_combo.setCurrentIndex(index)

    def _test_connections(self):
        """测试所有AI提供商连接"""
        self.test_btn.setText("测试中...")
        self.test_btn.setEnabled(False)

        # 这里可以添加异步测试连接的逻辑
        # 暂时显示一个简单的消息
        QMessageBox.information(self, "连接测试", "连接测试功能正在开发中...")

        self.test_btn.setText("测试连接")
        self.test_btn.setEnabled(True)

    def load_settings(self):
        """加载设置"""
        # 加载AI配置
        self.ai_config.load_config()

        # API设置 - 从新配置系统加载
        self.deepseek_key.setText(self.ai_config.get_api_key("deepseek"))
        self.gemini_key.setText(self.ai_config.get_api_key("gemini"))
        self.qianwen_key.setText(self.ai_config.get_api_key("qianwen"))
        self.openai_key.setText(self.ai_config.get_api_key("openai"))
        self.newapi_key.setText(self.ai_config.get_api_key("newapi"))

        # NewAPI URL设置
        newapi_config = self.ai_config.get_provider_config("newapi")
        if newapi_config:
            self.newapi_url.setText(newapi_config.base_url)

        # 代理设置 - 从旧配置系统加载（向后兼容）
        proxy = self.config.get_proxy()
        self.gemini_proxy_check.setChecked(bool(proxy.get("http") or proxy.get("https")))
        self.http_proxy.setText(proxy.get("http", ""))
        self.https_proxy.setText(proxy.get("https", ""))

        # 启用/禁用代理输入框
        self.http_proxy.setEnabled(self.gemini_proxy_check.isChecked())
        self.https_proxy.setEnabled(self.gemini_proxy_check.isChecked())

        # 默认提供商和模型
        default_provider = self.ai_config.settings.default_provider.value
        provider_index = self.provider_combo.findText(default_provider)
        if provider_index >= 0:
            self.provider_combo.setCurrentIndex(provider_index)
            self._on_provider_changed(default_provider)

        # 系统提示词
        self.system_prompt.setText(self.ai_config.settings.system_prompt)

        # 连接代理复选框信号
        self.gemini_proxy_check.stateChanged.connect(self._on_proxy_check_changed)

    def _on_proxy_check_changed(self, state):
        """处理代理复选框状态变化"""
        enabled = bool(state)
        self.http_proxy.setEnabled(enabled)
        self.https_proxy.setEnabled(enabled)
        if not enabled:
            self.http_proxy.clear()
            self.https_proxy.clear()

    def save_settings(self):
        """保存设置"""
        try:
            # 保存API密钥到新配置系统
            self.ai_config.set_api_key("deepseek", self.deepseek_key.text().strip())
            self.ai_config.set_api_key("gemini", self.gemini_key.text().strip())
            self.ai_config.set_api_key("qianwen", self.qianwen_key.text().strip())
            self.ai_config.set_api_key("openai", self.openai_key.text().strip())
            self.ai_config.set_api_key("newapi", self.newapi_key.text().strip())

            # 保存NewAPI URL
            newapi_config = self.ai_config.get_provider_config("newapi")
            if newapi_config:
                newapi_config.base_url = self.newapi_url.text().strip()
                self.ai_config.set_provider_config("newapi", newapi_config)

            # 保存默认提供商和模型
            selected_provider = self.provider_combo.currentText()
            if selected_provider:
                self.ai_config.settings.default_provider = AIProvider(selected_provider)

                # 更新选中提供商的模型
                provider_config = self.ai_config.get_provider_config(selected_provider)
                if provider_config and self.model_combo.currentText():
                    provider_config.model = self.model_combo.currentText()
                    provider_config.enabled = True  # 启用选中的提供商
                    self.ai_config.set_provider_config(selected_provider, provider_config)

            # 保存系统提示词
            self.ai_config.settings.system_prompt = self.system_prompt.toPlainText().strip()

            # 保存AI配置
            self.ai_config.save_config()

            # 向后兼容：同时保存到旧配置系统
            self.config.set_api_key("deepseek", self.deepseek_key.text().strip())
            self.config.set_api_key("gemini", self.gemini_key.text().strip())
            self.config.set_api_key("qianwen", self.qianwen_key.text().strip())

            # 代理设置（保存到旧配置系统）
            if self.gemini_proxy_check.isChecked():
                self.config.set_proxy(self.http_proxy.text().strip(), self.https_proxy.text().strip())
            else:
                self.config.set_proxy("", "")

            # 默认模型（保存到旧配置系统）
            self.config.config["default_model"] = selected_provider
            self.config.save_config()

            # 系统提示词（保存到旧配置系统）
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