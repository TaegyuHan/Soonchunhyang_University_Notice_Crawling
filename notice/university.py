from notice import Crawlling
from notice_code import UNIVERSITY


class UniversityNotice(Crawlling):
    """ 대학 공지 """

    _main_page_url = f"https://home.sch.ac.kr/sch/06/{UNIVERSITY}.jsp"

    def __init__(self, date: str, tag: str) -> None:
        """

        :param date: (날짜) "2022-07-20"
        :param tag: (단어) "키워드 단어 입력"

        처리해야할 문제
            - 날짜를 받으면 거기까지 데이터 뽑기
            - 뽑은 데이터 링크를 가지고 (또다시 크롤링)

        """
        self._main_page_response = self._request_get(self._main_page_url)
        self._start_page_number, self._end_page_number = \
            self._get_page_number(self._main_page_response)


if __name__ == '__main__':
    a = UniversityNotice(date="2022-07-19", tag="사랑")