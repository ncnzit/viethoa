import os
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)
CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'content', 'articles'))

def parse_markdown(filepath):
    """Phân tích metadata và nội dung từ file Markdown"""
    metadata = {
        'title': '',
        'date': '',
        'category': 'Game Việt hoá',
        'tags': [],
        'thumbnail': '',
        'slug': os.path.splitext(os.path.basename(filepath))[0]
    }
    content_lines = []
    
    if not os.path.exists(filepath):
        return metadata, ""

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Đọc phần đầu (metadata)
        in_metadata = True
        body_start = 0
        for i, line in enumerate(lines):
            line_str = line.strip()
            if not line_str and i > 0:
                # Dòng trống đầu tiên kết thúc metadata
                body_start = i
                break
            
            # Cắt các metadata fields
            match = re.match(r'^([a-zA-Z0-9_-]+)\s*:\s*(.*)$', line_str)
            if match:
                key = match.group(1).lower()
                val = match.group(2).strip()
                if key == 'title':
                    metadata['title'] = val
                elif key == 'date':
                    metadata['date'] = val
                elif key == 'category':
                    metadata['category'] = val
                elif key == 'tags':
                    metadata['tags'] = [t.strip() for t in val.split(',') if t.strip()]
                elif key == 'thumbnail':
                    metadata['thumbnail'] = val
            else:
                # Nếu gặp dòng không phải metadata format, coi như bắt đầu body
                body_start = i
                break
                
        content = "".join(lines[body_start:])
    except Exception as e:
        content = ""
        print(f"Error parsing {filepath}: {e}")
        
    return metadata, content.strip()

def write_markdown(filepath, metadata, content):
    """Ghi metadata và nội dung vào file Markdown"""
    tags_str = ", ".join(metadata.get('tags', []))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Title: {metadata.get('title', '')}\n")
        f.write(f"Date: {metadata.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}\n")
        f.write(f"Category: {metadata.get('category', 'Game Việt hoá')}\n")
        if tags_str:
            f.write(f"Tags: {tags_str}\n")
        if metadata.get('thumbnail'):
            f.write(f"Thumbnail: {metadata.get('thumbnail', '')}\n")
        f.write("\n")  # Dòng trống phân cách
        f.write(content)

@app.route('/')
def index():
    if not os.path.exists(CONTENT_DIR):
        os.makedirs(CONTENT_DIR, exist_ok=True)
        
    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    articles_data = []
    
    # Gom danh sách tags để hiển thị bộ lọc
    all_tags = set()
    
    for f in files:
        filepath = os.path.join(CONTENT_DIR, f)
        # Lấy thời gian chỉnh sửa file cuối cùng
        mtime = os.path.getmtime(filepath)
        mod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        
        meta, _ = parse_markdown(filepath)
        meta['filename'] = f
        meta['mod_date'] = mod_date
        articles_data.append(meta)
        
        for t in meta['tags']:
            all_tags.add(t)
            
    # Sắp xếp bài mới nhất lên đầu dựa trên thời gian sửa đổi (mtime)
    articles_data.sort(key=lambda x: x['mod_date'], reverse=True)
    
    return render_template('index.html', articles=articles_data, tags=sorted(list(all_tags)))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        slug = request.form.get('slug', title.lower().replace(" ", "-"))
        slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)  # clean slug
        
        filepath = os.path.join(CONTENT_DIR, f"{slug}.md")
        metadata = {
            'title': title,
            'date': request.form.get('date', datetime.now().strftime('%Y-%m-%d %H:%M')),
            'category': request.form.get('category', 'Game Việt hoá'),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'thumbnail': request.form.get('thumbnail', '')
        }
        content = request.form['content']
        write_markdown(filepath, metadata, content)
        return redirect(url_for('index'))
        
    return render_template('edit.html', is_new=True, filename="", content="", metadata={})

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if request.method == 'POST':
        title = request.form['title']
        metadata = {
            'title': title,
            'date': request.form.get('date', datetime.now().strftime('%Y-%m-%d %H:%M')),
            'category': request.form.get('category', 'Game Việt hoá'),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'thumbnail': request.form.get('thumbnail', '')
        }
        content = request.form['content']
        write_markdown(filepath, metadata, content)
        return redirect(url_for('index'))
        
    metadata, content = parse_markdown(filepath)
    return render_template('edit.html', is_new=False, filename=filename, content=content, metadata=metadata)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))


# ============== QUẢN LÝ THẺ (TAGS) ==============

def get_all_articles_meta():
    """Lấy metadata + content tất cả bài viết"""
    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    result = []
    for f in files:
        filepath = os.path.join(CONTENT_DIR, f)
        meta, content = parse_markdown(filepath)
        result.append((filepath, meta, content))
    return result

@app.route('/tags')
def tags():
    """Trang quản lý thẻ — đếm số bài viết mỗi thẻ"""
    tag_counts = {}
    for filepath, meta, content in get_all_articles_meta():
        for t in meta['tags']:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    # Sắp xếp theo số bài giảm dần
    tags_sorted = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
    return render_template('tags.html', tags=tags_sorted)

@app.route('/tags/rename', methods=['POST'])
def rename_tag():
    """Đổi tên thẻ trên toàn bộ bài viết"""
    old_tag = request.form['old_tag'].strip()
    new_tag = request.form['new_tag'].strip()
    if old_tag and new_tag:
        for filepath, meta, content in get_all_articles_meta():
            if old_tag in meta['tags']:
                meta['tags'] = [new_tag if t == old_tag else t for t in meta['tags']]
                # Loại bỏ trùng lặp giữ thứ tự
                seen = set()
                meta['tags'] = [t for t in meta['tags'] if not (t in seen or seen.add(t))]
                write_markdown(filepath, meta, content)
    return redirect(url_for('tags'))

@app.route('/tags/delete', methods=['POST'])
def delete_tag():
    """Xoá thẻ khỏi toàn bộ bài viết"""
    tag = request.form['tag'].strip()
    if tag:
        for filepath, meta, content in get_all_articles_meta():
            if tag in meta['tags']:
                meta['tags'] = [t for t in meta['tags'] if t != tag]
                write_markdown(filepath, meta, content)
    return redirect(url_for('tags'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
