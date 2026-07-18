#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""验证所有依赖包是否已正确安装。"""

import sys
import io
from importlib import import_module

# 设置正确的编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify_dependencies():
    """验证依赖包安装情况。"""
    
    print("=" * 70)
    print("[Package Verification Tool]")
    print("=" * 70)
    print()
    
    # 定义所有必需的包
    dependencies = [
        ('requests', 'HTTP client library'),
        ('feedparser', 'RSS/Atom parser'),
        ('dotenv', 'Environment variable management'),
        ('bs4', 'HTML parser (BeautifulSoup4)'),
        ('urllib3', 'HTTP connection pool'),
    ]
    
    print("Checking dependencies...")
    print()
    
    all_ok = True
    installed = []
    missing = []
    
    for package_name, description in dependencies:
        try:
            import_module(package_name)
            print(f"[OK] {package_name:<15} - {description}")
            installed.append(package_name)
        except ImportError:
            print(f"[FAIL] {package_name:<15} - {description}")
            missing.append(package_name)
            all_ok = False
    
    print()
    print("=" * 70)
    print()
    
    # 统计结果
    print(f"[OK] Installed: {len(installed)} packages")
    for pkg in installed:
        print(f"   - {pkg}")
    
    if missing:
        print()
        print(f"[FAIL] Missing: {len(missing)} packages")
        for pkg in missing:
            print(f"   - {pkg}")
        
        print()
        print("[INFO] Install missing packages:")
        print("   pip install -r requirements.txt")
        print()
        return False
    
    print()
    print("=" * 70)
    print("[OK] All dependencies are installed correctly!")
    print("=" * 70)
    print()
    
    # 验证可以导入爬虫模块
    print("Verifying scraper modules...")
    try:
        from scrapers import NewsScraper
        print("[OK] Can import NewsScraper")
    except Exception as e:
        print(f"[FAIL] Cannot import NewsScraper: {e}")
        return False
    
    print()
    print("[SUCCESS] All checks passed!")
    print()
    
    return True

if __name__ == '__main__':
    success = verify_dependencies()
    sys.exit(0 if success else 1)
