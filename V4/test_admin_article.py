import os
import time, pytest

from V4.admin_article_page import ArticleAddTask
from utils import TDD


class TestAdminArticle(object):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\data" + "\\admin_essay_classify_data.csv"

    def setup_class(self):
        self.article_add_task = ArticleAddTask()

    def teardown_class(self):
        self.article_add_task.driver_quit()

    # 输入空 slug
    @pytest.mark.parametrize('title, father, slug, expected, code', TDD.get_admin_essay_classify_data(path))
    def test_invalidcase(self, title, father, slug, expected, code):
        self.article_add_task.go_to(title, father, slug, expected, code)


if __name__ == '__main__':
    pytest.mian(['-sv', 'test_admin_login.py', 'test_admin_article.py'])
    # pytest.mian(['-sv', 'test_admin_login.py'])
