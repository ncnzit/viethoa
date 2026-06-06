import os
import json
from datetime import date
from blinker import signal

PUBLISH = os.environ.get("PUBLISH") == "true"
SITEURL = "https://viethoa.nguyez.com" if PUBLISH else "http://localhost:8000"
SITEURL_MAIN = SITEURL
CANONICAL_URL = "https://viethoa.nguyez.com"
AUTHOR = "nguyez"
SITENAME = "Việt Hoá Game"
KEYWORDS = "việt hoá game, viet hoa game, patch việt hoá, game tiếng việt, nguyez"
DESCRIPTION = "Tổng hợp các bản Việt hoá game, thông tin patch, nền tảng, trạng thái và hướng dẫn cài đặt."
DEFAULT_DATE_FORMAT = "%d/%m/%Y"
COPYRIGHT_YEAR = 2026

with open("authors.json", encoding="utf-8") as f:
    AUTHORS_INFO = json.load(f)

PATH = "content"
ARTICLE_PATHS = ["articles"]
PAGE_PATHS = ["pages"]
OUTPUT_PATH = "output"
STATIC_PATHS = ["images", "extra", "files"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt", "template": True},
    "extra/humans.txt": {"path": "humans.txt", "template": True},
    "extra/ads.txt": {"path": "ads.txt"},
    "extra/CNAME": {"path": "CNAME"},
    "extra/manifest.json": {"path": "manifest.json"},
}

DEFAULT_LANG = "vi"
TIMEZONE = "Asia/Ho_Chi_Minh"
LOCALE = ["vi_VN.UTF-8", "vi_VN.utf8", "vi_VN", "Vietnamese_Vietnam.1258", "en_US.UTF-8", "C.UTF-8", "C"]
DATE_FORMATS = {"vi": ("vi_VN.UTF-8", "%d/%m/%Y")}
I18N_SUBSITES = {}

ARTICLE_URL = "{slug}/"
ARTICLE_SAVE_AS = "{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
CATEGORY_URL = "danh-muc/{slug}/"
CATEGORY_SAVE_AS = "danh-muc/{slug}/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
AUTHOR_URL = "tac-gia/{slug}/"
AUTHOR_SAVE_AS = "tac-gia/{slug}/index.html"
ARCHIVES_URL = "luu-tru/"
ARCHIVES_SAVE_AS = "luu-tru/index.html"
TAGS_URL = "tags/"
TAGS_SAVE_AS = "tags/index.html"
AUTHORS_URL = "tac-gia/"
AUTHORS_SAVE_AS = "tac-gia/index.html"
CATEGORIES_URL = "danh-muc/"
CATEGORIES_SAVE_AS = "danh-muc/index.html"
DRAFT_URL = "drafts/{slug}/"
DRAFT_SAVE_AS = "drafts/{slug}/index.html"

DEFAULT_PAGINATION = 10
PAGINATION_PATTERNS = (
    (1, "{base_name}/", "{base_name}/index.html"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)
PAGINATED_TEMPLATES = {"index": None, "tag": None, "category": None, "author": None}

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = "feeds/all.atom.xml"
FEED_ALL_RSS = "feeds/all.rss.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
CATEGORY_FEED_RSS = "feeds/{slug}.rss.xml"
FEED_JSON = "feed.json"
FEED_SAVE_AS = "feed.json"

THEME = "themes/AliBaba"
THEME_STATIC_PATHS = ["static"]
TEMPLATE_EXTENSIONS = [".html.j2", ".html"]
BROWSER_COLOR = "#ef4444"
PYGMENTS_STYLE = "dracula"
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

NAVBAR_LINKS = [
    {"name": "Trang chủ", "url": "/", "target": "_self", "icon": "fa-solid fa-house"},
    {"name": "Hướng dẫn", "url": "/gioi-thieu/", "target": "_self", "icon": "fa-solid fa-file-alt"},
    {"name": "Game Việt hoá", "url": "/tag/viet-hoa/", "target": "_self", "icon": "fa-solid fa-fire"},
    {"name": "Tìm kiếm", "url": "#", "target": "_self", "icon": "fa-solid fa-search"},
    {"name": "Thẻ", "url": "/tags/", "target": "_self", "icon": "fa-solid fa-tags"},
    {"name": "Ủng hộ", "url": "https://donate.nguyez.com/", "target": "_blank", "icon": "fa-solid fa-heart", "color": "#fbbf24"},
]
MENUITEMS = [
    ("Trang chủ", "/"),
    ("Danh mục", "/danh-muc/"),
    ("Thẻ", "/tags/"),
    ("Lưu trữ", "/luu-tru/"),
]
FEATURED_ARTICLE = {
    "title": "Chào mừng đến với Việt Hoá Game",
    "slug": "chao-mung",
    "category": "Thông báo",
    "summary": "Trang tổng hợp các bản Việt hoá game.",
    "date": "2026-06-06",
}

PLUGIN_PATHS = ["plugins"]
PLUGINS = [
    "plugins.i18n_subsites",
    "plugins.sitemap",
    "pelican.plugins.neighbors",
    "plugins.series",
    "plugins.fix_sitemap",
    "plugins.json_feed",
    "plugins.responsive_image_shortcode",
    "plugins.search",
    "plugins.pelican_redirect",
    "plugins.video_schema",
    "plugins.pelican-toc",
    "plugins.related_posts",
    "plugins.baba_stats",
    "plugins.extract_linked_metadata",
]
SERIES_DEFAULT_INDEXING = "date"
SERIES_PAGE_INDEXING = "title"
SEARCH_MODE = "output"
SEARCH_HTML_SELECTOR = "main"
SEARCH_LIMIT = 10
FORMATTED_FIELDS = ["summary", "content"]

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.fenced_code": {},
        "markdown.extensions.tables": {},
        "markdown.extensions.toc": {"permalink": "#"},
        "markdown.extensions.admonition": {},
        "markdown.extensions.attr_list": {},
        "markdown.extensions.footnotes": {},
    },
    "output_format": "html5",
}
TOC = {"TOC_HEADERS": "^h[1-3]", "TOC_RUN": "true", "TOC_INCLUDE_TITLE": "false"}

SEO_REPORT = False
SEO_ENHANCER = False
SEO_ENHANCER_OPEN_GRAPH = False
SEO_ENHANCER_TWITTER_CARDS = False
GOOGLE_ANALYTICS = ""
GTM_ID = ""
GOOGLE_ADSENSE = ""
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.7, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
    "exclude": [r"page/", r"^noindex/", r"\.json$", r"\.txt$", r"404\.html"],
}
ROBOTS = "index, follow"

DISQUS_SITENAME = ""
SOCIAL = {
    "github": "ncnzit",
    "bynogame": "https://donate.nguyez.com",
}
MASTODON = {"username": "", "instance": "mastodon.social"}
LINKS = {"Donate": "https://donate.nguyez.com", "GitHub": "https://github.com/ncnzit/viethoa"}

DEVELOPMENT_MODE = False
DELETE_OUTPUT_DIRECTORY = True
CACHE_CONTENT = False
CHECK_MODIFIED_METHOD = "sha1"
LOAD_CONTENT_CACHE = False
GZIP_CACHE = False
JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
tmpsig = signal("tmpsig")
I18N_FILTER_SIGNALS = [tmpsig]
WITH_FUTURE_DATES = True
USE_FOLDER_AS_CATEGORY = False
WEBASSETS_DEBUG = False
MAIN_MENU = True
RELATED_POSTS_MAX = 4
SUMMARY_MAX_LENGTH = 160
DEFAULT_CATEGORY = "Thông báo"
ARTICLE_EDIT_LINK = "https://github.com/ncnzit/viethoa/edit/main/content/articles/%(slug)s.md"
COMMENTS_ENABLED = False
ENHANCE_META = True
ADMIN_TOOLS = False
VERSION = "1.0.0"
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True
USE_LESS = True
JINJA_GLOBALS = {"AUTHORS_INFO": AUTHORS_INFO, "current_year": date.today().year, "current_date": date.today()}
IGNORE_FILES = ["404.html", ".#&", "flycheck_*", "flymake_*"]
DEFAULT_PAGESCHEMA = "article"
HOME_HIDE_TAGS = True
REDIRECTS = {}
