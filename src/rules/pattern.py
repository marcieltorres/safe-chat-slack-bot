from re import Pattern as PatternCompiled
from re import compile, fullmatch
from typing import List

from src.rules.constants import CPF_REGEX_PATTERN, EMAIL_REGEX_PATTERN, PHONE_REGEX_PATTERN
from src.rules.validators import is_valid_cpf


class Pattern:
    __slots__ = ['compiled_pattern', 'rules']
    compiled_pattern: PatternCompiled
    rules: List

    def __init__(self) -> None:
        self.rules = []
        self.rules.append(CPF_REGEX_PATTERN)
        self.rules.append(EMAIL_REGEX_PATTERN)
        self.rules.append(PHONE_REGEX_PATTERN)
        self.compile_all_rules()

    def compile_all_rules(self) -> PatternCompiled:
        self.compiled_pattern = compile(r'|'.join(self.rules))

    def find_all(self, text) -> int:
        count = 0
        for match in self.compiled_pattern.finditer(text):
            matched = match.group(0)
            # The CPF regex is only a first pass: an 11-digit sequence
            # that fails the check digits is not a CPF. It still counts
            # if it is also a valid phone number (e.g. 11999999999);
            # otherwise it is ignored instead of raising a warning.
            if (
                fullmatch(CPF_REGEX_PATTERN, matched)
                and not is_valid_cpf(matched)
                and not fullmatch(PHONE_REGEX_PATTERN, matched)
            ):
                continue
            count += 1
        return count


pattern = Pattern()
