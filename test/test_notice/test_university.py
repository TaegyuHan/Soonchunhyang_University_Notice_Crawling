import unittest

from notice.university import UniversityNotice


class TestUniversityNotice(unittest.TestCase):

    def setUp(self):
        """ 공지 인스턴스 생성 """

    def test_init_university(self):
        """  """
        self._un = UniversityNotice(date="2022-07-20",
                                    tag="예비군")