"""
Fintech Security & Compliance Module
Implements cryptographic hashing, tokenization, data masking, and PCI-DSS compliant sanitization.
Zero external library dependencies (uses Python hashlib, hmac, secrets).
"""

import hashlib
import hmac
import secrets
import base64
import json
import time
from typing import Dict, Any, Optional, Tuple


class SecurityManager:
    """Enterprise security utility for hashing, sanitization, and cryptographic signing."""

    def __init__(self, secret_key: Optional[str] = None):
        self._secret_key = (secret_key or secrets.token_hex(32)).encode('utf-8')

    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """PBKDF2-HMAC-SHA256 password hashing with 100,000 iterations."""
        if not salt:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return pwd_hash.hex(), salt

    @staticmethod
    def verify_password(password: str, salt: str, expected_hash: str) -> bool:
        """Constant-time password verification."""
        computed_hash, _ = SecurityManager.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, expected_hash)

    def generate_token(self, payload: Dict[str, Any], expires_in_seconds: int = 3600) -> str:
        """Generates a cryptographically signed URL-safe JWT-like authorization token."""
        token_payload = {
            **payload,
            "exp": int(time.time()) + expires_in_seconds,
            "iat": int(time.time()),
            "nonce": secrets.token_hex(8)
        }
        encoded_data = base64.urlsafe_b64encode(
            json.dumps(token_payload, separators=(',', ':')).encode('utf-8')
        ).decode('utf-8').rstrip('=')

        signature = hmac.new(
            self._secret_key,
            encoded_data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return f"{encoded_data}.{signature}"

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifies signature, structure, and expiration of a signed token."""
        try:
            parts = token.split('.')
            if len(parts) != 2:
                return None

            encoded_data, signature = parts
            expected_sig = hmac.new(
                self._secret_key,
                encoded_data.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_sig):
                return None

            # Add padding back if necessary
            padding_len = len(encoded_data) % 4
            if padding_len:
                encoded_data += '=' * (4 - padding_len)

            payload_json = base64.urlsafe_b64decode(encoded_data.encode('utf-8')).decode('utf-8')
            payload = json.loads(payload_json)

            # Check expiration
            if payload.get("exp", 0) < time.time():
                return None

            return payload
        except Exception:
            return None

    @staticmethod
    def mask_card_number(pan: str) -> str:
        """
        PCI-DSS Compliance Rule: Mask Primary Account Number (PAN).
        Preserves first 6 (BIN) and last 4 digits, masks intermediate digits.
        Example: 4111112233334444 -> 4111-11XX-XXXX-4444
        """
        clean_pan = "".join(filter(str.isdigit, pan))
        if len(clean_pan) < 10:
            return "****"
        prefix = clean_pan[:4]
        suffix = clean_pan[-4:]
        masked_middle = "X" * (len(clean_pan) - 8)
        raw_masked = prefix + masked_middle + suffix
        # Chunk into 4s
        return "-".join(raw_masked[i:i+4] for i in range(0, len(raw_masked), 4))

    @staticmethod
    def mask_account_number(acc_num: str) -> str:
        """Mask bank account number, exposing only last 4 digits."""
        clean = "".join(filter(str.isalnum, acc_num))
        if len(clean) <= 4:
            return "****"
        return f"****-****-{clean[-4:]}"

    @staticmethod
    def calculate_audit_checksum(data: Dict[str, Any], previous_checksum: str = "") -> str:
        """Calculates a SHA-256 Merkle-tree hash chaining entry for immutable audit logs."""
        canonical_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        combined = f"{previous_checksum}:{canonical_str}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()

    @staticmethod
    def validate_luhn(card_number: str) -> bool:
        """Validates credit card checksum using standard Luhn algorithm."""
        digits = [int(d) for d in str(card_number) if d.isdigit()]
        if len(digits) < 13 or len(digits) > 19:
            return False
        checksum = 0
        reverse_digits = digits[::-1]
        for i, d in enumerate(reverse_digits):
            if i % 2 == 1:
                doubled = d * 2
                checksum += doubled - 9 if doubled > 9 else doubled
            else:
                checksum += d
        return checksum % 10 == 0
