import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# Đảm bảo đường dẫn đến content articles là tuyệt đối
CONTENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'content', 'articles'))

@app.route('/')
def index():
    # Liệt kê tất cả file .md
    articles = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')]
    return render_template('index.html', articles=articles)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit(filename):
    filepath = os.path.join(CONTENT_DIR, filename)
    if request.method == 'POST':
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(request.form['content'])
        return redirect(url_for('index'))
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('edit.html', filename=filename, content=content)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        title = request.form['title']
        slug = title.lower().replace(" ", "-")
        filepath = os.path.join(CONTENT_DIR, f"{slug}.md")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nCategory: Game Việt hoá\nTags: việt hoá\nThumbnail: \n\n{request.form['content']}")
        return redirect(url_for('index'))
    return render_template('new.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
