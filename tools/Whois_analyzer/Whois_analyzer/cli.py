"""
WHOIS Domain Analyzer - Giao diện dòng lệnh
"""

import os
import sys
import argparse
import logging
from typing import List, Dict, Optional

from . import analyzer, utils

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_parser() -> argparse.ArgumentParser:
    """
    Tạo parser cho giao diện dòng lệnh
    
    Returns:
        argparse.ArgumentParser: Parser đã được cấu hình
    """
    parser = argparse.ArgumentParser(
        description='WHOIS Domain Analyzer - Công cụ truy vấn và phân tích thông tin WHOIS',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Lệnh')
    
    # Lệnh tra cứu đơn lẻ
    single_parser = subparsers.add_parser('single', help='Tra cứu thông tin WHOIS cho một tên miền')
    single_parser.add_argument('domain', help='Tên miền cần tra cứu')
    single_parser.add_argument('-o', '--output', help='Tệp đầu ra (định dạng JSON)')
    single_parser.add_argument('-t', '--timeout', type=int, default=10, help='Thời gian chờ tối đa (giây) cho truy vấn WHOIS')
    
    # Lệnh tra cứu hàng loạt
    batch_parser = subparsers.add_parser('batch', help='Tra cứu thông tin WHOIS cho nhiều tên miền')
    batch_parser.add_argument('input_file', help='Tệp chứa danh sách tên miền (mỗi tên miền trên một dòng)')
    batch_parser.add_argument('-o', '--output', help='Tệp đầu ra (CSV hoặc JSON)')
    batch_parser.add_argument('-f', '--format', choices=['csv', 'json'], default='csv', help='Định dạng đầu ra (mặc định: csv)')
    batch_parser.add_argument('-w', '--workers', type=int, default=5, help='Số luồng xử lý đồng thời (mặc định: 5)')
    batch_parser.add_argument('-t', '--timeout', type=int, default=10, help='Thời gian chờ tối đa (giây) cho mỗi truy vấn WHOIS')
    
    return parser

def handle_single_query(args):
    """
    Xử lý lệnh tra cứu đơn lẻ
    
    Args:
        args: Các đối số dòng lệnh
    """
    domain = args.domain.lower()
    
    # Kiểm tra tính hợp lệ của tên miền
    if not utils.validate_domain(domain):
        logger.error(f"Tên miền không hợp lệ: {domain}")
        sys.exit(1)
    
    # Tạo đối tượng phân tích và thực hiện truy vấn
    whois_analyzer = analyzer.WhoisAnalyzer(timeout=args.timeout)
    result = whois_analyzer.query_domain(domain)
    
    # Hiển thị kết quả
    print(utils.format_whois_result(result))
    
    # Lưu kết quả nếu được yêu cầu
    if args.output:
        utils.save_to_json([result], args.output)
        logger.info(f"Đã lưu kết quả vào: {args.output}")

def handle_batch_query(args):
    """
    Xử lý lệnh tra cứu hàng loạt
    
    Args:
        args: Các đối số dòng lệnh
    """
    try:
        # Đọc danh sách tên miền
        domains = utils.parse_domain_list(args.input_file)
        if not domains:
            logger.error("Không tìm thấy tên miền hợp lệ trong tệp đầu vào")
            sys.exit(1)
        
        logger.info(f"Đã đọc {len(domains)} tên miền từ {args.input_file}")
        
        # Tạo đối tượng phân tích và thực hiện truy vấn hàng loạt
        whois_analyzer = analyzer.WhoisAnalyzer(timeout=args.timeout)
        results = whois_analyzer.batch_query(domains, max_workers=args.workers)
        
        # Lưu kết quả
        if args.output:
            if args.format.lower() == 'csv':
                utils.save_to_csv(results, args.output)
            else:
                utils.save_to_json(results, args.output)
            logger.info(f"Đã lưu kết quả vào: {args.output}")
        else:
            # Hiển thị tóm tắt nếu không có tệp đầu ra
            print(f"\nKết quả truy vấn cho {len(domains)} tên miền:")
            success_count = sum(1 for r in results if r.get('status') == 'success')
            error_count = len(results) - success_count
            print(f"- Thành công: {success_count}")
            print(f"- Lỗi: {error_count}")
            
            # Hiển thị thông tin chi tiết cho một số tên miền đầu tiên
            print("\nChi tiết một số kết quả đầu tiên:")
            for i, result in enumerate(results[:3]):  # Chỉ hiển thị 3 kết quả đầu tiên
                print(f"\n--- Kết quả {i+1} ---")
                print(utils.format_whois_result(result))
            
            # Hướng dẫn người dùng lưu kết quả
            print("\nĐể xem đầy đủ kết quả, hãy chạy lại lệnh với tham số --output")
    
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
        sys.exit(1)

def main():
    """
    Hàm chính xử lý giao diện dòng lệnh
    """
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == 'single':
        handle_single_query(args)
    elif args.command == 'batch':
        handle_batch_query(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()