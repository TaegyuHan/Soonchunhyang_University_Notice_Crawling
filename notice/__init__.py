import requests
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus
from bs4 import BeautifulSoup
import bs4


class Crawlling:
    """ 크롤링 요청 클래스 """

    _REQUEST_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    def _request_get(self, url: str) -> requests.models.Response:
        """ request get 요청 """
        response = requests.get(url=url,
                                headers=self._REQUEST_HEADER)
        if response.status_code == HTTPStatus.OK:
            return response
        else:
            raise Exception('Response Status Code is not 200!')

    def _remove_span_tags(self, tag: bs4.element.Tag) -> str:
        """ span 들어있는 tag span 지우기 """
        tag.span.decompose()
        return tag.text.strip()

    def _strip_tags(self, tag: bs4.element.Tag) -> str:
        """ span 안 들어있는 tag """
        return tag.text.strip()

    def _get_url(self, tag: bs4.element.Tag) -> str:
        """ a tag 의 href 링크 얻기 """
        return tag["href"]

    def _get_table_rows(self, url: str) -> list[tuple[str, str, str, ...]]:
        """ 테이블 row 리스트 얻기 """
        response = self._request_get(url)

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find("table", {"class": "type_board"})  # table tag

        # td tags
        td_seq_list = list(map(lambda x: self._strip_tags(x), table.find_all("td", {"class": "seq"})))
        td_subject_list = list(map(lambda x: self._strip_tags(x), table.find_all("td", {"class": "subject"})))
        td_url_list = list(map(lambda x: self._get_url(x), table.find_all("a")))
        td_writer_list = list(map(lambda x: self._remove_span_tags(x), table.find_all("td", {"class": "writer"})))
        td_date_list = list(map(lambda x: self._remove_span_tags(x), table.find_all("td", {"class": "date"})))
        td_hits_list = list(map(lambda x: self._remove_span_tags(x), table.find_all("td", {"class": "hits"})))

        row_list = zip(
            td_seq_list,
            td_subject_list,
            td_url_list,
            td_writer_list,
            td_date_list,
            td_hits_list
        )

        return row_list

    def _get_page_number(self, response: requests.models.Response) -> tuple[int, int]:
        """ (시작, 끝) 페이지 숫자 얻기 """
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        a_tag = soup.find("a", {"class": "pager last"})  # table tag
        url = a_tag["href"]
        querys = parse_qs(urlparse(url).query)

        return 10, int(querys["pager.offset"][0])