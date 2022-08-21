AUTHOR = 'n4okins'
SITENAME = 'blog'
SITEURL = 'https://n4okins.github.io/blog'

STATIC_PATHS = [
    'static/assets',
]
EXTRA_PATH_METADATA = {
    'static/assets/HackGenConsoleNFJ-Regular.ttf': {'path': 'theme/fonts/HackGenConsoleNFJ-Regular.ttf'},
    'static/assets/robots.txt': {'path': 'robots.txt'},
    'static/assets/favicon.ico': {'path': 'favicon.ico'},  # and this
    'static/assets/CNAME': {'path': 'CNAME'},
    'static/assets/LICENSE': {'path': 'LICENSE'},
    'static/assets/README': {'path': 'README'},
}
THEME = "addons/basic"

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'

# https://docs.getpelican.com/en/latest/settings.html

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = ()

DEFAULT_PAGINATION = 10

FILENAME_METADATA = '(?P<title>.*)'
DEFAULT_DATE = "fs"

DELETE_OUTPUT_DIRECTORY = True


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True