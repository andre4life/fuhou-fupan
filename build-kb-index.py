#!/usr/bin/env python3
"""
访后复盘引擎 — 知识库预索引构建脚本
扫描保险知识库目录，生成 kb-index.json（供前端纯静态检索）
"""
import os
import json
import re
import sys

KB_DIR = os.path.join(os.path.dirname(__file__), '..', '保险知识库')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'public')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'kb-index.json')

# 话题关键词映射（与前端 extractTopicsForKB 保持一致）
TOPIC_KEYWORDS = {
    '养老': ['养老', '退休', '年金', '养老金'],
    '教育': ['教育', '子女', '孩子', '上学'],
    '健康': ['健康', '医疗', '重疾', '大病', '医保'],
    '传承': ['传承', '继承', '遗产', '受益人', '遗嘱'],
    '婚姻': ['婚姻', '离婚', '夫妻', '婚内', '婚前'],
    '企业': ['企业', '公司', '债务', '隔离', '家企'],
    '房产': ['房产', '房子', '房屋', '不动产'],
    '社保': ['社保', '医保', '养老金', '退休金'],
    '纠纷': ['纠纷', '理赔', '拒赔', '诉讼', '判决'],
    '产品': ['收益', '回报', '利率', '分红', 'IRR', '万能'],
    '法律': ['法律', '法条', '民法典', '保险法', '司法解释'],
    '跨境': ['跨境', '香港', '境外', '外币', '离岸'],
    '话术': ['话术', '切入', '沟通', '异议', '销售'],
    '保险认知': ['没钱', '太贵', '预算', '紧张', '不划算'],
    '纠纷案例': ['案例', '故事', '经历', '判决书'],
}

def build_index():
    if not os.path.exists(KB_DIR):
        print(f'错误：知识库目录不存在 {KB_DIR}')
        sys.exit(1)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    index = []
    errors = []
    
    def scan(dir_path, category):
        try:
            items = os.listdir(dir_path)
        except PermissionError:
            return
        for item in sorted(items):
            full_path = os.path.join(dir_path, item)
            if os.path.isdir(full_path):
                scan(full_path, item)
            elif item.endswith('.md'):
                rel_path = os.path.relpath(full_path, KB_DIR)
                title = item[:-3].replace('_', ' ')
                content = ''
                snippet = ''
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read(5000)  # 只读前5000字符
                    snippet = re.sub(r'[\r\n]+', ' ', content[:300]).strip()
                except Exception as e:
                    errors.append(f'{rel_path}: {e}')
                
                entry = {
                    'path': rel_path.replace('\\', '/'),
                    'category': category or '',
                    'filename': item,
                    'title': title,
                    'snippet': snippet[:300],
                    'fullContent': content[:2000]
                }
                index.append(entry)
    
    scan(KB_DIR, '')
    
    # 写入
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(index),
            'builtAt': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'items': index
        }, f, ensure_ascii=False, indent=2)
    
    print(f'✅ 知识库索引已构建')
    print(f'   源目录: {KB_DIR}')
    print(f'   输出: {OUTPUT_FILE}')
    print(f'   文件数: {len(index)}')
    print(f'   大小: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB')
    if errors:
        print(f'   警告: {len(errors)} 个文件读取失败')
        for e in errors[:5]:
            print(f'       {e}')

if __name__ == '__main__':
    build_index()
