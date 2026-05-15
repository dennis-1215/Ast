
class NewsService:
    def __init__(self, api):
        self.api = api
        self.news_index = 0

    def get_news_data(self):
        # 뉴스 호출 및 저장
        api_news = self.api.get_market_news()

        if api_news:
            self.news_data = api_news
        else:
            # API 실패 시 보여줄 기본 데이터 (백업용)
            self.news_data = [{"title": "📢 실시간 뉴스를 불러올 수 없습니다.", "url": ""}]

        return self.news_data
