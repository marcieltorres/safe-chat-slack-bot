from re import Pattern as PatternCompiled
from re import compile
from typing import List

from rules.constants import CPF_REGEX_PATTERN, EMAIL_REGEX_PATTERN


class Pattern:
    __slots__ = ['compiled_pattern', 'rules']
    compiled_pattern: PatternCompiled
    rules: List

    def __init__(self) -> None:
        self.rules = []
        self.rules.append(CPF_REGEX_PATTERN)
        self.rules.append(EMAIL_REGEX_PATTERN)
        self.compile_all_rules()

    def compile_all_rules(self) -> PatternCompiled:
        self.compiled_pattern = compile(r'|'.join(self.rules))

    def find_all(self, text) -> int:
        return len(self.compiled_pattern.findall(text))


pattern = Pattern()
