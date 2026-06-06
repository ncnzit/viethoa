# Công cụ quản lý bài viết Việt Hoá Game

## Cài đặt & Sử dụng

### Cách 1: Click file start.bat (Dễ nhất)
1. Mở thư mục `tools/`
2. Double-click `start.bat`
3. Trình duyệt sẽ tự mở ra `http://localhost:5000`
4. Bạn có thể viết/sửa bài viết ngay

### Cách 2: Chạy trực tiếp (Terminal)
```bash
cd tools
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install Flask
python app.py
```
Sau đó truy cập `http://localhost:5000` trên trình duyệt.

---

## Hướng dẫn sử dụng

### 1. Trang chủ (/)
- **Danh sách bài viết:** Hiển thị tất cả file `.md` trong `content/articles/`
- **Nút "Tạo bài mới":** Click để mở form viết bài với Markdown editor
- **Nút "Sửa":** Click để chỉnh sửa bài viết cũ

### 2. Tạo bài mới (/new)
1. Nhập **Tiêu đề bài viết**
2. Viết nội dung trong **SimpleMDE Editor** (editor Markdown chuyên nghiệp)
   - **Bold:** `**text**` hoặc click nút Bold
   - **Italic:** `*text*` hoặc click nút Italic
   - **Heading:** `## Tiêu đề` hoặc click nút Heading
   - **Link:** `[Text](url)` hoặc click nút Link
   - **Ảnh:** `![Alt](url)` hoặc click nút Image
   - **Preview:** Click tab "Preview" để xem trước
3. Click "Tạo bài" → File `.md` được tạo tự động trong `content/articles/`

Metadata tự động được thêm:
```
Title: Tiêu đề của bạn
Date: 2026-06-06 12:34
Category: Game Việt hoá
Tags: việt hoá
Thumbnail: 
```

### 3. Sửa bài viết (/edit/<filename>)
1. Click "Sửa" trên trang chủ
2. Chỉnh sửa nội dung trong editor
3. Click "Lưu" → Lưu tự động vào file

---

## Cấu trúc Metadata Markdown

Mỗi file `.md` bắt đầu với metadata YAML:

```markdown
Title: Tiêu đề bài viết
Date: 2026-06-06 12:34
Category: Game Việt hoá
Tags: việt hoá, patch, action-rpg
Thumbnail: /images/1.jpg
Summary: Đoạn tóm tắt ngắn gọn (tùy chọn)

Nội dung bài viết viết bằng Markdown...
```

### Các trường bắt buộc:
- **Title:** Tiêu đề bài viết
- **Date:** Ngày viết (format: YYYY-MM-DD HH:MM)
- **Category:** Danh mục (thường là "Game Việt hoá")
- **Tags:** Thẻ ngăn cách bằng dấu phẩy

### Các trường tùy chọn:
- **Thumbnail:** Đường dẫn ảnh thumbnail `/images/ten_file.jpg`
- **Summary:** Tóm tắt bài viết (hiển thị ở card)

---

## Upload ảnh

1. Đặt ảnh vào thư mục `S:\2026 - Github - mm\viethoa\content\images\`
2. Trong bài viết, dùng đường dẫn tương đối:
   ```markdown
   ![Mô tả ảnh](/images/ten_file.jpg)
   ```
3. Nếu dùng làm Thumbnail:
   ```
   Thumbnail: /images/ten_file.jpg
   ```

---

## Quy trình deploy

Sau khi viết/sửa bài xong:

### Cách 1: Tự động (Được khuyến cáo)
1. Mở terminal tại thư mục `viethoa/`
2. Chạy:
   ```bash
   git add .
   git commit -m "feat: Thêm bài viết mới (Tên bài)"
   git push
   ```
3. GitHub Actions tự động build & deploy lên `viethoa.nguyez.com`

### Cách 2: Preview local trước
1. Terminal tại `viethoa/` chạy:
   ```bash
   pelican --listen
   ```
2. Truy cập `http://localhost:8000` để xem preview
3. Nếu ổn, mới push lên GitHub

---

## Troubleshooting

### "start.bat không chạy được"
- Kiểm tra Python đã cài chưa: `python --version`
- Nếu chưa, tải Python từ https://python.org (chọn "Add Python to PATH")
- Restart cmd/terminal sau khi cài Python

### "Port 5000 đang dùng"
- Tìm process dùng port 5000 và tắt nó, hoặc
- Chỉnh sửa `app.py`, dòng cuối thành `app.run(port=5001)`

### "File .md không lưu được"
- Kiểm tra quyền ghi trong thư mục `content/articles/`
- Hoặc chạy terminal với quyền Admin

---

## Ghi chú kỹ thuật

- **Framework:** Flask (Python web framework nhẹ)
- **Editor:** SimpleMDE (Markdown editor chuyên nghiệp)
- **Styling:** Tailwind CSS (hiện đại, dark mode)
- **Database:** Không cần - dùng file hệ thống
- **Deploy:** GitHub Actions tự động build Pelican & deploy GitHub Pages
