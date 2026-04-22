#!/usr/bin/env python3
"""
验证和修复公司官网URL
"""

import pandas as pd
import requests
import time
import re
from urllib.parse import urlparse
from datetime import datetime

def verify_url(url):
    """验证URL是否可访问"""
    if not url or pd.isna(url) or str(url).strip() == '':
        return False, 'URL为空'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            return True, f'可访问 (状态码: {response.status_code})'
        else:
            return False, f'不可访问 (状态码: {response.status_code})'
    except requests.exceptions.ConnectionError as e:
        return False, f'连接错误: {str(e)[:50]}'
    except Exception as e:
        return False, f'错误: {str(e)[:50]}'

def generate_possible_urls(company_name):
    """生成可能的公司官网URL"""
    urls = []
    
    # 提取公司名中的关键部分
    # 移除"株式会社"、"合同会社"等前缀
    clean_name = company_name
    prefixes = ['株式会社', '合同会社', '有限会社', '合資会社', '合名会社']
    for prefix in prefixes:
        if clean_name.startswith(prefix):
            clean_name = clean_name[len(prefix):]
            break
    
    # 移除括号内容
    clean_name = re.sub(r'[（(].*?[）)]', '', clean_name)
    clean_name = clean_name.strip()
    
    # 生成可能的域名
    possible_names = []
    
    # 1. 完整公司名（罗马字）
    # 这里应该使用真正的罗马字转换，暂时用简单方法
    romaji_name = clean_name.lower()
    possible_names.append(romaji_name)
    
    # 2. 公司名缩写（取首字母或前几个字符）
    if len(clean_name) > 2:
        possible_names.append(clean_name[:3])
        possible_names.append(clean_name[:4])
    
    # 3. 常见日本公司域名模式
    domains = ['.co.jp', '.jp', '.com', '.net', '.org']
    
    for name in possible_names:
        for domain in domains:
            urls.append(f'https://www.{name}{domain}')
            urls.append(f'https://{name}{domain}')
    
    # 添加一些特定公司的已知域名
    known_companies = {
        'バンコム': ['vcom', 'bankom', 'bancom'],
        'プレミアムアーツ': ['premium-arts'],
        'ウェルネット': ['wellnet'],
        'HashiCorp Japan': ['hashicorp'],
        'H.U.グループ中央研究所': ['hu-group'],
        'アイサス': ['aisas'],
        'アイザックシステムズ': ['isaacsys'],
        'エスディーピー': ['sdp'],
        'ソナー': ['sonar'],
        'KYCOMホールディングス': ['kycom-hd'],
        'IGG Japan': ['igg'],
        'Retail AI': ['retail-ai'],
        'ルミテック': ['lumitec'],
        'エクウス': ['equus']
    }
    
    for key, values in known_companies.items():
        if key in company_name:
            for value in values:
                for domain in domains:
                    urls.append(f'https://www.{value}{domain}')
                    urls.append(f'https://{value}{domain}')
    
    return list(set(urls))  # 去重

def find_correct_website(company_name, current_url):
    """查找正确的公司官网"""
    print(f"查找 {company_name} 的正确官网...")
    
    # 首先验证当前URL
    if current_url and not pd.isna(current_url):
        is_valid, message = verify_url(current_url)
        if is_valid:
            print(f"  当前URL有效: {current_url}")
            return current_url, True
    
    # 生成可能的URL并测试
    possible_urls = generate_possible_urls(company_name)
    print(f"  生成 {len(possible_urls)} 个可能的URL")
    
    tested_count = 0
    for url in possible_urls[:20]:  # 只测试前20个
        tested_count += 1
        is_valid, message = verify_url(url)
        if is_valid:
            print(f"  找到有效URL: {url}")
            return url, True
        
        if tested_count % 5 == 0:
            print(f"  已测试 {tested_count}/{len(possible_urls[:20])} 个URL")
    
    print(f"  未找到有效URL")
    return current_url, False

def main():
    print("开始验证和修复公司官网URL...")
    print("=" * 80)
    
    # 读取文件
    input_file = 'input_companies_final.csv'
    df = pd.read_csv(input_file)
    
    print(f"处理 {len(df)} 家公司")
    print()
    
    results = []
    fixed_count = 0
    
    for idx, row in df.iterrows():
        company = row['公司名']
        current_url = row.get('官网URL', '')
        
        print(f"{idx+1}/{len(df)}: {company}")
        print(f"  当前URL: {current_url}")
        
        # 验证当前URL
        if current_url and not pd.isna(current_url):
            is_valid, message = verify_url(current_url)
            print(f"  验证结果: {message}")
            
            if not is_valid:
                # 尝试查找正确的URL
                new_url, found = find_correct_website(company, current_url)
                if found and new_url != current_url:
                    print(f"  修复URL: {new_url}")
                    current_url = new_url
                    fixed_count += 1
                    url_status = '已修复'
                    url_note = f'原URL无效，已找到新URL'
                else:
                    url_status = '无效'
                    url_note = f'URL无效且未找到替代'
            else:
                url_status = '有效'
                url_note = message
        else:
            print(f"  无当前URL，尝试查找...")
            new_url, found = find_correct_website(company, '')
            if found:
                current_url = new_url
                fixed_count += 1
                url_status = '已找到'
                url_note = '成功找到官网URL'
            else:
                url_status = '未找到'
                url_note = '无法找到官网URL'
        
        # 保存结果
        results.append({
            '公司名': company,
            '官网URL': current_url,
            '問い合わせURL': row.get('問い合わせURL', ''),
            '备注': row.get('备注', ''),
            'URL状态': url_status,
            'URL备注': url_note,
            '检索时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        print()
        time.sleep(1)  # 避免请求过快
    
    # 创建新的DataFrame
    result_df = pd.DataFrame(results)
    
    # 保存到新文件
    output_file = 'input_companies_verified.csv'
    result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print("=" * 80)
    print(f"处理完成！")
    print(f"  总共处理: {len(df)} 家公司")
    print(f"  修复/找到: {fixed_count} 家公司的官网URL")
    print(f"  结果已保存到: {output_file}")
    
    # 显示统计
    status_counts = result_df['URL状态'].value_counts()
    print("\n状态统计:")
    for status, count in status_counts.items():
        print(f"  {status}: {count} 家")
    
    return result_df

if __name__ == "__main__":
    main()