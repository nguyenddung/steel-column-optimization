# 🏗️ Steel Column Optimization

## 📖 Giới thiệu
Đây là dự án mình thực hiện từ năm nhất 🎓.  
Mục tiêu là **tối ưu hoá tiết diện cột thép Kingpost** trong công trình Top-Down tại Trường Đại học Xây dựng.  

- Áp dụng **thuật toán tiến hoá vi phân (Differential Evolution - DE)**.  
- Mở rộng thêm biến thể **GDE (Greedy Differential Evolution)** để tăng tốc độ hội tụ.  
- Đáp ứng **các điều kiện kỹ thuật** về bền, ổn định, và khả năng chịu lực theo tiêu chuẩn xây dựng.  

🔗 Tham khảo thêm tại bài báo:  
[Nghiên cứu tối ưu hóa tiết diện cột chống tạm trong thi công tầng hầm bằng phương pháp Top-down](https://tapchixaydung.vn/nghien-cuu-toi-uu-hoa-tiet-dien-cot-chong-tam-trong-thi-cong-tang-ham-bang-phuong-phap-topdown-20201224000027940.html)

---

## 🚀 Tính năng
- Giao diện trực quan bằng **Tkinter**.  
- Nhập thông số tải trọng, kích thước, đặc trưng vật liệu.  
- Chạy thuật toán DE để tìm ra tiết diện cột thép **tối ưu về diện tích và đảm bảo an toàn**.  
- Kiểm tra tự động các điều kiện kỹ thuật:  
  - Bền nén, bền cắt.  
  - Độ ổn định tổng thể.  
  - Điều kiện kích thước hợp lệ.  

---

## 🛠️ Cài đặt

### Yêu cầu
- Python 3.x ([Download](https://www.python.org/downloads/))
- Thư viện chuẩn `tkinter`, `math`, `random` (có sẵn trong Python).  

### Cách chạy
Clone project và chạy file Python:

```bash
git clone https://github.com/yourusername/steel-column-optimization.git
cd steel-column-optimization
python SteelColumnOptimization.py
Ứng dụng Tkinter sẽ mở ra giao diện nhập liệu và tính toán.
```
📊 Các thông số đầu vào

N: Lực dọc (daN)

V: Lực cắt (daN)

Mx, My: Moment uốn theo 2 phương (daN.cm)

D: Đường kính cọc khoan (mm)

L0: Chiều dài cột (m)

F: Hệ số khuếch đại (DE parameter)

Cr: Chỉ số lai ghép (DE parameter)

Số vòng lặp: Population size / Iterations

Thông số vật liệu: cường độ chịu kéo, chịu cắt, mô đun đàn hồi E, hệ số an toàn γc.

🧮 Thuật toán sử dụng

Differential Evolution (DE):

Sinh quần thể ngẫu nhiên các phương án tiết diện.

Lai ghép và đột biến để sinh nghiệm mới.

Lựa chọn dựa trên hàm mục tiêu (diện tích tiết diện nhỏ nhất thoả mãn điều kiện kỹ thuật).

Hàm mục tiêu:

<img width="441" height="59" alt="image" src="https://github.com/user-attachments/assets/75e288e2-ad39-4d58-b899-ab4583893a02" />
📌 Kết quả

Xuất ra kích thước cột thép tối ưu:

Chiều cao bụng (Hc).

Bản cánh (Bf).

Bản cánh dày (Tf).

Bản bụng dày (Tw).

Tính toán diện tích tiết diện.

👨‍💻 Tác giả

Nguyễn Đức Dũng – FPT University

Nghiên cứu & ứng dụng từ năm nhất 🎓
