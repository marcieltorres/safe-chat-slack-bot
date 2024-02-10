import os
from unittest import TestCase, mock

from src.config.settings import Settings


class SettingsTest(TestCase):
    def setUp(self) -> None:
        self.settings = Settings(file='./tests/config/settings_to_test.conf')

    def test_get_setting_value_with_success(self):
        self.assertEqual(self.settings.get('app_name'), 'app-name')

    def test_get_default_value_when_setting_not_found_with_success(self):
        self.assertEqual(self.settings.get('not_found_var', 'default_value'), 'default_value')

    def test_get_setting_int_value_with_success(self):
        self.assertEqual(int(self.settings.get('sample_of_int_var')), 10)

    def test_get_setting_float_value_with_success(self):
        self.assertEqual(float(self.settings.get('sample_of_float_var')), 10.10)

    @mock.patch.dict(os.environ, {'ENV': 'prod'}, clear=True)
    def test_get_setting_value_from_production_env_with_success(self):
        prod_settings = Settings(file='./tests/config/settings_to_test.conf')
        self.assertEqual(prod_settings.get('app_var'), 'prod-app-var')

    @mock.patch.dict(os.environ, {'ENV': 'qa'}, clear=True)
    def test_get_setting_value_from_qa_env_with_success(self):
        qa_settings = Settings(file='./tests/config/settings_to_test.conf')
        self.assertEqual(qa_settings.get('app_var'), 'qa-app-var')

    @mock.patch.dict(os.environ, {'ENV': 'test'}, clear=True)
    def test_get_setting_value_from_test_env_with_success(self):
        test_settings = Settings(file='./tests/config/settings_to_test.conf')
        self.assertEqual(test_settings.get('app_var'), 'test-app-var')

    @mock.patch.dict(os.environ, {'ENV': 'dev'}, clear=True)
    def test_get_setting_value_from_dev_env_with_success(self):
        dev_settings = Settings(file='./tests/config/settings_to_test.conf')
        self.assertEqual(dev_settings.get('app_var'), 'dev-app-var')
