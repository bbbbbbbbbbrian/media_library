class BaseParse():
    def can_handle(self, url):
        raise NotImplementedError

    def get_latest_chapter(self, series_url):
        raise NotImplementedError