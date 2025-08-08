#!/usr/bin/env python3
"""
配置迁移脚本 - 将旧配置迁移到新的AI配置系统
"""
import sys
import json
from pathlib import Path
from core.config_manager import ConfigManager
from core.ai_config import AIConfigManager
from core.ai_types import AIProvider

def migrate_config():
    """迁移配置"""
    print("开始配置迁移...")
    
    try:
        # 加载旧配置
        old_config = ConfigManager()
        print("✓ 旧配置加载成功")
        
        # 创建新配置管理器
        ai_config = AIConfigManager()
        print("✓ 新配置系统初始化成功")
        
        # 迁移API密钥
        providers = ["deepseek", "gemini", "qianwen"]
        for provider in providers:
            api_key = old_config.get_api_key(provider)
            if api_key:
                ai_config.set_api_key(provider, api_key)
                print(f"✓ 迁移 {provider} API密钥")
        
        # 迁移系统提示词
        system_prompt = old_config.get_system_prompt()
        if system_prompt:
            ai_config.settings.system_prompt = system_prompt
            print("✓ 迁移系统提示词")
        
        # 迁移默认模型
        default_model = old_config.config.get("default_model", "deepseek")
        if default_model in ["deepseek", "gemini", "qianwen"]:
            ai_config.settings.default_provider = AIProvider(default_model)
            print(f"✓ 迁移默认模型: {default_model}")
        
        # 迁移代理设置
        proxy = old_config.get_proxy()
        if proxy.get("http") or proxy.get("https"):
            for provider_name in ai_config.settings.providers:
                ai_config.settings.providers[provider_name].proxy = proxy
            print("✓ 迁移代理设置")
        
        # 保存新配置
        ai_config.save_config()
        print("✓ 新配置保存成功")
        
        # 备份旧配置
        backup_path = Path("data/config_backup.json")
        if old_config.config_file.exists():
            import shutil
            shutil.copy2(old_config.config_file, backup_path)
            print(f"✓ 旧配置已备份到: {backup_path}")
        
        print("\n🎉 配置迁移完成！")
        print("\n新功能:")
        print("- 支持OpenAI和NewAPI提供商")
        print("- 更灵活的模型配置")
        print("- 连接测试功能")
        print("- 预设提示词模板")
        print("- 流式响应支持")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置迁移失败: {e}")
        return False

def check_config_status():
    """检查配置状态"""
    print("检查配置状态...")
    
    # 检查旧配置
    old_config_path = Path("data/config.json")
    ai_config_path = Path("data/ai_config.json")
    
    print(f"旧配置文件: {'存在' if old_config_path.exists() else '不存在'}")
    print(f"新配置文件: {'存在' if ai_config_path.exists() else '不存在'}")
    
    if old_config_path.exists():
        try:
            with open(old_config_path, 'r', encoding='utf-8') as f:
                old_data = json.load(f)
            
            # 检查API密钥
            api_keys = old_data.get("ai_settings", {})
            configured_providers = []
            for provider, config in api_keys.items():
                if config.get("api_key"):
                    configured_providers.append(provider)
            
            print(f"已配置的提供商: {', '.join(configured_providers) if configured_providers else '无'}")
            print(f"默认模型: {old_data.get('default_model', '未设置')}")
            print(f"系统提示词: {'已设置' if old_data.get('system_prompt') else '未设置'}")
            
        except Exception as e:
            print(f"读取旧配置失败: {e}")
    
    if ai_config_path.exists():
        try:
            ai_config = AIConfigManager()
            enabled_providers = ai_config.get_enabled_providers()
            print(f"新配置已启用提供商: {', '.join(enabled_providers) if enabled_providers else '无'}")
            print(f"默认提供商: {ai_config.settings.default_provider.value}")
            
        except Exception as e:
            print(f"读取新配置失败: {e}")

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_config_status()
    else:
        print("WeChatAI 配置迁移工具")
        print("=" * 40)
        
        # 检查配置状态
        check_config_status()
        print()
        
        # 询问是否迁移
        response = input("是否要迁移配置？(y/N): ").strip().lower()
        if response in ['y', 'yes']:
            if migrate_config():
                print("\n迁移完成！请重启应用程序以使用新配置。")
            else:
                print("\n迁移失败，请检查错误信息。")
        else:
            print("取消迁移。")

if __name__ == "__main__":
    main()
