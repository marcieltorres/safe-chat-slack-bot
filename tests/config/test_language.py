from unittest import TestCase

from src.config.language import Language


class LanguageTest(TestCase):
    def test_translate_hello_message_to_pt_br(self):
        language = Language(lang='pt_BR')
        self.assertEqual(language.translate('Hello'), 'Olá')

    def test_translate_hello_message_to_en(self):
        language = Language(lang='en')
        self.assertEqual(language.translate('Hello'), 'Hello')

    def test_translate_hello_message_to_default_when_language_is_not_supported(self):
        language = Language(lang='foo')
        self.assertEqual(language.translate('Hello'), 'Hello')
