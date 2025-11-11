"""
테스트 모듈 초기화
"""
import sys
import os

# 프로젝트 루트를 Python path에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, 'app')

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if app_path not in sys.path:
    sys.path.insert(0, app_path)