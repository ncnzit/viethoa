import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pelicanconf import *

PUBLISH = True
SITEURL = "https://viethoa.nguyez.com"
SITEURL_MAIN = SITEURL
CANONICAL_URL = SITEURL
FEED_DOMAIN = SITEURL
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
