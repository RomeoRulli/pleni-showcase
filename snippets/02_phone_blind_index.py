"""Phone numbers at rest: encrypted for reading, blind-indexed for lookup.

Excerpt from `app/core/security.py`. Comments and messages translated from Portuguese; code unchanged.

A phone number is never stored in clear text. The row holds a Fernet ciphertext (to send a message) and
an HMAC-SHA256 blind index (to find the user by the number a message came from, with an indexed lookup
and without decrypting the table).
"""


def generate_brazilian_phone_variants(normalized_phone: str) -> list[str]:
    """Canonical variants for Brazilian mobile numbers (+55 + area code + 8 or 9 digits).

    WhatsApp sometimes reports a Brazilian number without the ninth digit (12 digits) while Planning Center
    has it with 13, or the other way round. This lets the lookup try both blind indexes.
    """
    variants = [normalized_phone]
    if normalized_phone.startswith("55"):
        if len(normalized_phone) == 12:
            # 55 + area code + 8 digits -> add the variant with the ninth digit
            with_nine = f"{normalized_phone[:4]}9{normalized_phone[4:]}"
            variants.append(with_nine)
        elif len(normalized_phone) == 13 and normalized_phone[4] == "9":
            # 55 + area code + 9 + 8 digits -> add the variant without the ninth digit
            without_nine = f"{normalized_phone[:4]}{normalized_phone[5:]}"
            variants.append(without_nine)
    return variants


def mask_phone(phone: str) -> str:
    """Masked form of the phone, safe for logs."""
    digits = _NON_DIGITS_RE.sub("", phone or "")
    if len(digits) < 8:
        return "***"
    return f"+{digits[:4]}*****{digits[-4:]}"


def compute_phone_blind_index(phone: str, blind_index_key: str) -> str:
    """Deterministic blind index (HMAC-SHA256) of a normalized phone number."""
    normalized = normalize_phone(phone)
    key_bytes = blind_index_key.encode("utf-8")
    msg_bytes = normalized.encode("utf-8")
    return hmac.new(key_bytes, msg_bytes, hashlib.sha256).hexdigest()


class PhoneCipher:
    """Authenticated encryption (Fernet: AES-128-CBC + HMAC-SHA256) for phones in SQLite."""

    def __init__(self, fernet_key: str) -> None:
        self._fernet = Fernet(fernet_key.encode("utf-8"))

    def encrypt_phone(self, phone: str) -> str:
        """Normalizes and encrypts the phone number for storage."""
        normalized = normalize_phone(phone)
        token = self._fernet.encrypt(normalized.encode("utf-8"))
        return token.decode("utf-8")

    def decrypt_phone(self, encrypted_phone: str) -> str:
        """Decrypts and authenticates the stored phone number."""
        try:
            plaintext = self._fernet.decrypt(encrypted_phone.encode("utf-8"))
            return plaintext.decode("utf-8")
        except InvalidToken as exc:
            raise SecurityError(
                "Integrity failure decrypting a phone from SQLite (wrong key or tampered data)."
            ) from exc
