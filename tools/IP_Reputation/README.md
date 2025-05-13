# IP Reputation Checker using VirusTotal

Công cụ kiểm tra danh tiếng địa chỉ IP sử dụng API của VirusTotal.

## Tính năng chính

- Tra cứu thông tin chi tiết về địa chỉ IP từ cơ sở dữ liệu VirusTotal
- Hiển thị báo cáo chi tiết với đánh giá từ nhiều nhà cung cấp bảo mật
- Lưu kết quả tra cứu vào tệp báo cáo định dạng JSON
- Giao diện dòng lệnh thân thiện với người dùng
- Hiển thị đẹp mắt với thư viện Rich
- **Chế độ hàng loạt** để kiểm tra nhiều địa chỉ IP cùng một lúc
- Tạo báo cáo tổng hợp CSV và JSON

## Yêu cầu

- Python 3.6 trở lên
- API key của VirusTotal (đăng ký miễn phí tại [VirusTotal](https://www.virustotal.com/))

## Cài đặt

1. Clone dự án hoặc tải xuống các tệp
2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chế độ đơn lẻ

```bash
python vt_ip_reputation.py <địa_chỉ_ip> [options]
```

#### Các tùy chọn cho chế độ đơn lẻ

- `-k, --api-key`: Chỉ định API key của VirusTotal (hoặc đặt biến môi trường `VT_API_KEY`)
- `-o, --output`: Tệp đầu ra để lưu báo cáo (định dạng JSON)
- `-q, --quiet`: Chế độ yên lặng - chỉ lưu báo cáo mà không hiển thị kết quả
- `-b, --batch`: Chuyển sang chế độ hàng loạt (hướng dẫn sử dụng batch_ip_checker.py)

### Chế độ hàng loạt

```bash
python batch_ip_checker.py [options]
```

#### Các tùy chọn cho chế độ hàng loạt

- `-i, --ip`: Danh sách các địa chỉ IP cần kiểm tra (cách nhau bởi dấu cách)
- `-f, --file`: Tệp chứa danh sách các địa chỉ IP (mỗi dòng một địa chỉ)
- `-o, --output-dir`: Thư mục để lưu các báo cáo riêng lẻ và báo cáo tổng hợp
- `-d, --delay`: Thời gian chờ giữa các yêu cầu API (mặc định: 15 giây)
- `-k, --api-key`: API key của VirusTotal
- `-q, --quiet`: Chế độ yên lặng - chỉ hiển thị tiến trình và tóm tắt

## Ví dụ

### Chế độ đơn lẻ

```bash
# Kiểm tra địa chỉ IP với API key được cung cấp
python vt_ip_reputation.py 8.8.8.8 --api-key YOUR_API_KEY

# Kiểm tra địa chỉ IP và lưu báo cáo
python vt_ip_reputation.py 8.8.8.8 --output report.json

# Sử dụng biến môi trường cho API key
export VT_API_KEY=your_api_key
python vt_ip_reputation.py 8.8.8.8
```

### Chế độ hàng loạt

```bash
# Kiểm tra nhiều địa chỉ IP từ dòng lệnh
python batch_ip_checker.py -i 8.8.8.8 1.1.1.1 9.9.9.9 -o reports/

# Kiểm tra nhiều địa chỉ IP từ tệp
python batch_ip_checker.py -f examples/sample_ip_list.txt -o reports/

# Giảm thời gian chờ giữa các yêu cầu (lưu ý giới hạn API)
python batch_ip_checker.py -f examples/sample_ip_list.txt -o reports/ -d 10

# Sử dụng chế độ yên lặng để chỉ hiển thị tiến trình và tóm tắt
python batch_ip_checker.py -f examples/sample_ip_list.txt -o reports/ -q
```

## Cấu trúc dự án

```
ip-reputation-checker/
├── vt_ip_reputation.py   # Công cụ kiểm tra đơn lẻ
├── batch_ip_checker.py   # Công cụ kiểm tra hàng loạt
├── requirements.txt     # Các thư viện phụ thuộc
├── README.md           # Tài liệu dự án
├── tests/              # Các thử nghiệm đơn vị
│   ├── test_vt_ip_reputation.py
│   └── sample_response.json
└── examples/           # Các ví dụ mẫu
    ├── example_usage.py
    └── sample_ip_list.txt
```

## Lưu ý

- API miễn phí của VirusTotal có giới hạn 4 yêu cầu mỗi phút
- Chế độ hàng loạt tự động thêm thời gian chờ giữa các yêu cầu để tuân thủ giới hạn API
- Đảm bảo sử dụng công cụ này cho mục đích hợp pháp và tuân thủ điều khoản sử dụng của VirusTotal