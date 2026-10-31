def is_valid_cpf(candidate: str) -> bool:
    """Validate a CPF candidate by its check digits.

    The regex in constants.py is only a cheap first pass: any 11-digit
    sequence matches it, including order IDs, timestamps and phone
    numbers. A candidate counts as a CPF only if its two check digits
    (dígitos verificadores) are correct. Sequences of a single repeated
    digit (00000000000, 11111111111, ...) are never valid CPFs.
    """
    digits = [int(d) for d in candidate if d.isdigit()]

    if len(digits) != 11 or len(set(digits)) == 1:
        return False

    for position in (9, 10):
        checksum = sum(d * w for d, w in zip(digits[:position], range(position + 1, 1, -1)))
        expected = (checksum * 10 % 11) % 10
        if digits[position] != expected:
            return False

    return True
