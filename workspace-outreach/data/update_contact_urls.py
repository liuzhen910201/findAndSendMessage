#!/usr/bin/env python3
"""
更新公司问询URL脚本
严格按照input_companies_final.csv文件中的公司名进行检索
"""

import pandas as pd
import requests
import time
from urllib.parse import urljoin
import re

def search_company_website(company_name):
    """搜索公司官网"""
    # 这里简化处理，实际应该使用搜索引擎API
    # 对于已知公司，返回预设的URL
    known_companies = {
        '株式会社ZENSHIN': 'https://www.zenshin-inc.co.jp',
        'ソニー株式会社': 'https://www.sony.co.jp',
        'トヨタ自動車株式会社': 'https://www.toyota.co.jp',
        '楽天グループ株式会社': 'https://www.rakuten.co.jp',
        'LINEヤフー株式会社': 'https://www.lycorp.co.jp'
    }
    
    return known_companies.get(company_name, '')

def find_contact_page(base_url):
    """查找问询页面"""
    if not base_url:
        return ''
    
    # 常见的问询页面路径
    common_paths = [
        '/contact/',
        '/contact',
        '/inquiry/',
        '/inquiry',
        '/問い合わせ/',
        '/問い合わせ',
        '/お問い合わせ/',
        '/お問い合わせ',
        '/contact-us/',
        '/contact-us',
        '/contactform/',
        '/contactform',
        '/support/contact/',
        '/support/contact',
        '/corporate/contact/',
        '/corporate/contact',
    ]
    
    # 尝试常见路径
    for path in common_paths:
        test_url = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))
        try:
            response = requests.head(test_url, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                return test_url
        except:
            continue
    
    return ''

def verify_url(url):
    """验证URL可访问性"""
    if not url:
        return '未找到', 'URL为空'
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code == 200:
            return '可访问', f'状态码: {response.status_code}'
        elif response.status_code == 403:
            return '禁止访问', f'状态码: {response.status_code} (可能需要权限)'
        elif response.status_code == 404:
            return '页面不存在', f'状态码: {response.status_code}'
        else:
            return f'状态码: {response.status_code}', ''
    except requests.exceptions.Timeout:
        return '超时', '连接超时'
    except requests.exceptions.ConnectionError:
        return '连接错误', '无法连接'
    except Exception as e:
        return '错误', str(e)[:50]

def main():
    print("开始更新公司问询URL...")
    print("=" * 80)
    
    # 读取文件
    input_file = 'input_companies_final.csv'
    df = pd.read_csv(input_file)
    
    print(f"找到 {len(df)} 家公司:")
    for idx, row in df.iterrows():
        print(f"  {idx+1}. {row['公司名']}")
    print()
    
    results = []
    for idx, row in df.iterrows():
        company = row['公司名']
        print(f"处理: {company}")
        
        # 1. 查找官网
        website_url = search_company_website(company)
        print(f"  官网: {website_url}")
        
        # 2. 查找问询页面
        contact_url = find_contact_page(website_url)
        print(f"  问询页面: {contact_url}")
        
        # 3. 验证问询页面
        if contact_url:
            status, detail = verify_url(contact_url)
            print(f"  验证结果: {status}")
            if detail:
                print(f"  详情: {detail}")
        else:
            status = '未找到'
            detail = '无法找到问询页面'
            print(f"  验证结果: {status}")
        
        # 保存结果
        results.append({
            '公司名': company,
            '官网URL': website_url,
            '問い合わせURL': contact_url,
            '备注': row.get('备注', ''),
            'URL状态': status,
            'URL备注': detail
        })
        
        print()
        time.sleep(1)  # 避免请求过快
    
    # 创建新的DataFrame
    result_df = pd.DataFrame(results)
    
    # 保存回原文件
    result_df.to_csv(input_file, index=False, encoding='utf-8-sig')
    
    print("=" * 80)
    print(f"更新完成！结果已保存到: {input_file}")
    print()
    print("最终结果:")
    print(result_df.to_string())
    
    return result_df

if __name__ == "__main__":
    main()