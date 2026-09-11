from .asura import AsuraParse

parsers = [
    AsuraParse(),
]

def get_latest_chapter(url):
    for parser in parsers:
        if parser.can_handle(url):
            return parser.get_latest_chapter(url)

    raise ValueError("Unsupported website")