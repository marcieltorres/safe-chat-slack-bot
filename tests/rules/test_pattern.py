from unittest import TestCase

from src.rules.pattern import Pattern


class PatternTest(TestCase):
    def setUp(self) -> None:
        self.pattern = Pattern()

    def test_if_text_can_be_a_cpf_with_success(self):
        self.assertEqual(self.pattern.find_all("11144477735"), 1)

    def test_if_text_can_be_a_cpf_formatted_with_success(self):
        self.assertEqual(self.pattern.find_all("111.444.777-35"), 1)

    def test_if_text_with_invalid_cpf_check_digits_is_ignored(self):
        self.assertEqual(self.pattern.find_all("12345678901"), 0)

    def test_if_text_with_repeated_digit_cpf_is_ignored(self):
        self.assertEqual(self.pattern.find_all("00000000000"), 0)
        self.assertEqual(self.pattern.find_all("000.000.000-00"), 0)
        self.assertEqual(self.pattern.find_all("11111111111"), 0)
        self.assertEqual(self.pattern.find_all("111.111.111-11"), 0)

    def test_if_text_with_invalid_cpf_that_is_a_phone_still_counts(self):
        self.assertEqual(self.pattern.find_all("11999999999"), 1)

    def test_if_text_can_be_an_email_with_success(self):
        self.assertEqual(self.pattern.find_all("teste@teste.com"), 1)

    def test_if_text_contains_emails_and_cpfs_with_success(self):
        random_text = """
            Lorem Ipsum is simply dummy text 00000000000 of the printing and
            typesetting industry. Lorem Ipsum bla@blablabla.com has been the industry's
            standard 111.111.111-11 dummy text ever since the 1500s 11111111111
        """
        # Only the email counts: all three digit sequences fail the
        # CPF check digits and are not valid phone numbers either.
        self.assertEqual(self.pattern.find_all(random_text), 1)

    def test_if_text_no_contains_emails_and_cpfs_with_success(self):
        random_text = """
            Lorem Ipsum is simply dummy text of the printing and
            typesetting industry. Lorem Ipsum has been the industry's
            standard1 dummy text ever since the 1500s
        """
        self.assertEqual(self.pattern.find_all(random_text), 0)

    def test_if_text_can_be_a_phone_with_success(self):
        self.assertEqual(self.pattern.find_all("11999999999"), 1)

    def test_if_text_can_be_a_phone_formatted_with_success(self):
        self.assertEqual(self.pattern.find_all("(11) 99999-9999"), 1)

    def test_if_text_can_be_a_phone_with_spaces(self):
        self.assertEqual(self.pattern.find_all("11 99999 9999"), 1)
