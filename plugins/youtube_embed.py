"""
YouTube Auto-Embed Plugin for Pelican
Tự động chuyển link YouTube thành iframe embed responsive
"""
import re
from pelican import signals

YOUTUBE_REGEX = re.compile(
    r'(?:https?://)?(?:www\.)?'
    r'(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)'
    r'([a-zA-Z0-9_-]{11})'
    r'(?:[?&][^\s]*)?'
)

EMBED_TEMPLATE = '''
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 1.5rem 0;">
    <iframe src="https://www.youtube.com/embed/{video_id}" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
</div>
'''

def embed_youtube(content):
    """Thay thế link YouTube bằng iframe embed"""
    if content._content:
        # Chỉ xử lý link YouTube đứng độc lập trên 1 dòng
        lines = content._content.split('\n')
        new_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Match mọi link YouTube không nằm trong thẻ HTML <a>
            if 'youtube.com' in stripped or 'youtu.be' in stripped:
                match = YOUTUBE_REGEX.search(stripped)
                if match and not stripped.startswith('<a'):
                    video_id = match.group(1)
                    new_lines.append(EMBED_TEMPLATE.format(video_id=video_id))
                    continue
            new_lines.append(line)
        
        content._content = '\n'.join(new_lines)

def register():
    signals.content_object_init.connect(embed_youtube)
