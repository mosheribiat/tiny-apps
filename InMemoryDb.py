import sys
from typing import Optional, Dict, List


class Value:
    def __init__(self, value: str, expiry: int = sys.maxsize):
        self.value = value
        self.expiry = expiry


class InMemoryDB:
    def __init__(self):
        self.store: Dict[str, Dict[str, Value]] = {}

    def _is_key_present(self, key: str) -> bool:
        return key in self.store

    def _is_field_present(self, key: str, field: str) -> bool:
        return self._is_key_present(key) and field in self.store[key]

    # --- Level 1 ---
    def set(self, key: str, field: str, value: str):
        if not self._is_key_present(key):
            self.store[key] = {}
        self.store[key][field] = Value(value)

    def get(self, key: str, field: str) -> Optional[str]:
        if not self._is_field_present(key, field):
            return None
        return self.store[key][field].value

    def delete(self, key: str, field: str) -> bool:
        if not self._is_field_present(key, field):
            return False
        del self.store[key][field]
        return True

    # --- Level 2 ---
    def scan(self, key: str) -> List[str]:
        if not self._is_key_present(key):
            return []
        result = [f"{field}({val.value})" for field, val in self.store[key].items()]
        return sorted(result)

    def scan_by_prefix(self, key: str, prefix: str) -> List[str]:
        if not self._is_key_present(key):
            return []
        result = [f"{field}({val.value})"
                  for field, val in self.store[key].items()
                  if field.startswith(prefix)]
        return sorted(result)

    # --- Level 3 ---
    def set_at(self, key: str, field: str, value: str, timestamp: int=sys.maxsize):
        if not self._is_key_present(key):
            self.store[key] = {}
        self.store[key][field] = Value(value, expiry=timestamp)

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int):
        if not self._is_key_present(key):
            self.store[key] = {}
        self.store[key][field] = Value(value, expiry=timestamp + ttl)

    def delete_at(self, key: str, field: str, timestamp: int) -> bool:
        if not self._is_field_present(key, field):
            return False
        val = self.store[key][field]
        del self.store[key][field]
        return timestamp <= val.expiry

    def get_at(self, key: str, field: str, timestamp: int) -> Optional[str]:
        if not self._is_field_present(key, field):
            return None
        val = self.store[key][field]
        return val.value if timestamp <= val.expiry else None

    def scan_at(self, key: str, timestamp: int) -> List[str]:
        if not self._is_key_present(key):
            return []
        result = [f"{field}({val.value})"
                  for field, val in self.store[key].items()
                  if timestamp <= val.expiry]
        return sorted(result)

    def scan_prefix_at(self, key: str, prefix: str, timestamp: int) -> List[str]:
        if not self._is_key_present(key):
            return []
        result = [f"{field}({val.value})"
                  for field, val in self.store[key].items()
                  if field.startswith(prefix) and timestamp <= val.expiry]
        return sorted(result)