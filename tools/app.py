import os
import re
import json
import subprocess
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'content', 'articles'))
IMAGE_UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'content', 'images'))
PAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'content', 'pages'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_markdown(filepath):
    metadata = {'title':'','date':'','category':'Game Việt hoá','tags':[],'thumbnail':'','slug':os.path.splitext(os.path.basename(filepath))[0]}
    if not os.path.exists(filepath): return metadata, ""
    try:
        with open(filepath,'r',encoding='utf-8') as f:
            raw_content = f.read()
        lines = raw_content.replace('\r\n','\n').split('\n')
        body_start = 0
        for i, line in enumerate(lines):
            line_str = line.strip()
            if not line_str and i > 0:
                body_start = i
                break
            match = re.match(r'^([a-zA-Z0-9_-]+)\s*:\s*(.*)$', line_str)
            if match:
                key = match.group(1).lower()
                val = match.group(2).strip()
                if key == 'title': metadata['title'] = val
                elif key == 'date': metadata['date'] = val
                elif key == 'category': metadata['category'] = val
                elif key == 'tags': metadata['tags'] = [t.strip() for t in val.split(',') if t.strip()]
                elif key == 'thumbnail': metadata['thumbnail'] = val
                elif key == 'slug': metadata['slug'] = val
            else:
                body_start = i
                break
        content = "\n".join(lines[body_start:])
    except Exception as e:
        content = ""
        print(f"Error parsing {filepath}: {e}")
    return metadata, content.strip()

def write_markdown(filepath, metadata, content):
    normalized_content = content.replace('\r\n','\n')
    tags_str = ", ".join(metadata.get('tags', []))
    with open(filepath,'w',encoding='utf-8') as f:
        f.write(f"Title: {metadata.get('title', '')}\n")
        f.write(f"Date: {metadata.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))}\n")
        f.write(f"Category: {metadata.get('category', 'Game Việt hoá')}\n")
        if tags_str:
            f.write(f"Tags: {tags_str}\n")
        if metadata.get('thumbnail'):
            f.write(f"Thumbnail: {metadata.get('thumbnail', '')}\n")
        if metadata.get('slug'):
            f.write(f"Slug: {metadata.get('slug', '')}\n")
        f.write("\n")
        f.write(normalized_content)

@app.route('/')
def index():
    if not os.path.exists(CONTENT_DIR): os.makedirs(CONTENT_DIR, exist_ok=True)
    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    articles_data = []
    all_tags = set()
    for f in files:
        filepath = os.path.join(CONTENT_DIR, f)
        mtime = os.path.getmtime(filepath)
        mod_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')
        meta, _ = parse_markdown(filepath)
        meta['filename'] = f
        meta['mod_date'] = mod_date
        articles_data.append(meta)
        for t in meta['tags']: all_tags.add(t)
    articles_data.sort(key=lambda x: x['mod_date'], reverse=True)
    return render_template('index.html', articles=articles_data, tags=sorted(list(all_tags)))

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        slug = request.form.get('slug', '').strip() or re.sub(r'[^a-zA-Z0-9-]', '', title.lower().replace(" ", "-"))
        filepath = os.path.join(CONTENT_DIR, f"{slug}.md")
        metadata = {
            'title': title,
            'date': request.form.get('date', datetime.now().strftime('%Y-%m-%d %H:%M')).replace('T', ' '),
            'category': request.form.get('category', 'Game Việt hoá'),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'thumbnail': request.form.get('thumbnail', ''),
            'slug': slug
        }
        write_markdown(filepath, metadata, request.form['content'])
        return redirect(url_for('index'))
    all_tags = set()
    for _, meta, _ in get_all_articles_meta():
        for t in meta['tags']: all_tags.add(t)
    return render_template('edit.html', is_new=True, filename="", content="", metadata={'date': datetime.now().strftime('%Y-%m-%dT%H:%M'), 'slug': ''}, all_tags=sorted(list(all_tags)))

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if request.method == 'POST':
        original_meta, _ = parse_markdown(filepath)
        metadata = {
            'title': request.form['title'],
            'date': request.form.get('date', '').replace('T', ' ') or original_meta.get('date', datetime.now().strftime('%Y-%m-%d %H:%M')),
            'category': request.form.get('category', 'Game Việt hoá'),
            'tags': [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()],
            'thumbnail': request.form.get('thumbnail', ''),
            'slug': request.form.get('slug', '')
        }
        write_markdown(filepath, metadata, request.form['content'])
        return redirect(url_for('index'))
    metadata, content = parse_markdown(filepath)
    if ' ' in metadata['date']: metadata['date'] = metadata['date'].replace(' ', 'T')
    all_tags = set()
    for _, meta, _ in get_all_articles_meta():
        for t in meta['tags']: all_tags.add(t)
    return render_template('edit.html', is_new=False, filename=filename, content=content, metadata=metadata, all_tags=sorted(list(all_tags)))

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if os.path.exists(filepath): os.remove(filepath)
    return redirect(url_for('index'))

@app.route('/git_push', methods=['POST'])
def git_push():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
        commit_msg = f"Admin: Content update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=repo_dir, check=True, capture_output=True)
        return jsonify({'status': 'success', 'message': 'Đẩy lên website thành công! GitHub Actions đang build...'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': f'Lỗi Git: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Lỗi hệ thống: {str(e)}'}), 500

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(IMAGE_UPLOAD_FOLDER, filename))
        return jsonify({'url': f'/images/{filename}'}), 200
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/pages')
def pages():
    files = [f for f in os.listdir(PAGES_DIR) if f.endswith('.md')]
    pages_data = []
    for f in files:
        filepath = os.path.join(PAGES_DIR, f)
        meta, _ = parse_markdown(filepath)
        meta['filename'] = f
        pages_data.append(meta)
    return render_template('pages.html', pages=pages_data)

@app.route('/pages/edit/<filename>', methods=['GET', 'POST'])
def edit_page(filename):
    filepath = os.path.join(PAGES_DIR, filename)
    if request.method == 'POST':
        metadata = {
            'title': request.form['title'],
            'slug': request.form.get('slug', '').strip() or os.path.splitext(filename)[0]
        }
        write_markdown(filepath, metadata, request.form['content'])
        return redirect(url_for('pages'))
    metadata, content = parse_markdown(filepath)
    if ' ' in metadata.get('date', ''): metadata['date'] = metadata['date'].replace(' ', 'T')
    return render_template('edit_page.html', filename=filename, content=content, metadata=metadata)

@app.route('/tags')
def tags():
    tag_counts = {}
    for filepath, meta, content in get_all_articles_meta():
        for t in meta['tags']: tag_counts[t] = tag_counts.get(t, 0) + 1
    return render_template('tags.html', tags=sorted(tag_counts.items(), key=lambda x: (-x[1], x[0])))

@app.route('/tags/rename', methods=['POST'])
def rename_tag():
    old, new = request.form['old_tag'].strip(), request.form['new_tag'].strip()
    if old and new:
        for filepath, meta, content in get_all_articles_meta():
            if old in meta['tags']:
                meta['tags'] = list(set([new if t == old else t for t in meta['tags']]))
                write_markdown(filepath, meta, content)
    return redirect(url_for('tags'))

@app.route('/tags/delete', methods=['POST'])
def delete_tag():
    tag = request.form['tag'].strip()
    if tag:
        for filepath, meta, content in get_all_articles_meta():
            if tag in meta['tags']:
                meta['tags'] = [t for t in meta['tags'] if t != tag]
                write_markdown(filepath, meta, content)
    return redirect(url_for('tags'))

@app.route('/tags/add', methods=['POST'])
def add_tag():
    new_tag = request.form['new_tag'].strip()
    if new_tag:
        # Lưu tag vào file JSON để dùng làm gợi ý
        tags_file = os.path.join(os.path.dirname(__file__), 'custom_tags.json')
        custom_tags = []
        if os.path.exists(tags_file):
            with open(tags_file, 'r', encoding='utf-8') as f:
                custom_tags = json.load(f)
        if new_tag not in custom_tags:
            custom_tags.append(new_tag)
            with open(tags_file, 'w', encoding='utf-8') as f:
                json.dump(custom_tags, f, ensure_ascii=False, indent=2)
    return redirect(url_for('tags'))

def get_all_articles_meta():
    files = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    return [(os.path.join(CONTENT_DIR, f), *parse_markdown(os.path.join(CONTENT_DIR, f))) for f in files]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
