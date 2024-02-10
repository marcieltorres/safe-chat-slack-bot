from unittest import TestCase

from src.main import hello


class MainTest(TestCase):
    def test_main_hello(self):
        self.assertEqual(hello(), "Hello")
