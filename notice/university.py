from datetime import datetime as dt

from notice import Crawlling
from notice.notice_code import UNIVERSITY


class UniversityNotice(Crawlling):
    """ 대학 공지 """

    _main_page_url = f"https://home.sch.ac.kr/sch/06/{UNIVERSITY}.jsp"
    _page_navigation = f"{_main_page_url}?mode=list&board_no=20090723152156588979&pager.offset="

    def __init__(self, date: str, tag: str) -> None:
        """
        :param tag: (단어) "키워드 단어 입력"

        - 키워드 검색하기
        - 크롤링 과부화 를 만들어 낼 수 있다.

        """
        self._date = date
        self._tag = tag
        self._main_page_response = self._request_get(self._main_page_url)
        self._start_page_number, self._end_page_number = self._get_page_number(self._main_page_response)
        self._table_details()

    def _table_page_urls(self) -> str:
        """ 테이블 page urls 반환 """
        for page_number in range(self._start_page_number,
                                 self._end_page_number,
                                 self.PAGE_TEMP):
            yield self._page_navigation + str(page_number)

    def _match_date_rows(self, date: str) -> tuple[str, str, str, ...]:
        """ 날짜에 맞는 공지사항 반환 """
        date_format = "%Y-%m-%d"
        row_datas = []
        for url in self._table_page_urls():
            for table_row_data in self._get_table_rows(url):
                if dt.strptime(table_row_data[4], date_format) \
                        < dt.strptime(date, date_format):
                    return row_datas
                row_datas.append(table_row_data)
        return row_datas

    def _table_details(self):
        """ 테이블 디테일 확인하기 """
        for row_data in self._match_date_rows(self._date):
            print(row_data)