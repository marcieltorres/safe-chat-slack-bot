from gettext import GNUTranslations, translation
from os import getenv


class Language:
    __slots__ = ['gnu_translations']
    gnu_translations: GNUTranslations

    def __init__(self,
                 domain: str = 'base',
                 locale_dir: str = './src/locales',
                 fallback: bool = True,
                 lang: str = getenv('LANGUAGE', 'pt_BR')):

        self.gnu_translations = translation(domain, locale_dir, fallback=fallback, languages=[lang])

    def translate(self, text: str) -> str:
        return self.gnu_translations.gettext(text)

language = Language()
