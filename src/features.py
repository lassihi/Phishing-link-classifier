from urllib.parse import urlparse, ParseResult
import re
import math
from collections import Counter

_IP_PATTERN = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

def is_HTTPS(parsed: ParseResult) -> int:
    return int(parsed.scheme == "https")

def is_IP(parsed: ParseResult) -> int:
    return int(bool(_IP_PATTERN.match(parsed.hostname))) if parsed.hostname else 0

def host_length(parsed: ParseResult) -> int:
    return len(parsed.hostname) if parsed.hostname else 0

def number_count(parsed: ParseResult) -> int:
    return sum(c.isdigit() for c in (parsed.hostname or ""))

def dot_count(parsed: ParseResult) -> int:
    return parsed.hostname.count(".") if parsed.hostname else 0

def hyphen_count(parsed: ParseResult) -> int:
    return parsed.hostname.count("-") if parsed.hostname else 0

def path_depth(parsed: ParseResult) -> int:
    return parsed.path.count("/") if parsed.path else 0

def has_params(parsed: ParseResult) -> int:
    return int(bool(parsed.query or parsed.params))

def entropy(parsed: ParseResult) -> float:
    host = parsed.hostname or ""
    if not host:
        return 0.0
    counts = Counter(host)
    length = len(host)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())

def extract_features(url: str) -> dict:
    parsed = urlparse(url)
    return {
        "is_HTTPS": is_HTTPS(parsed),
        "is_domain": is_IP(parsed),
        "host_length": host_length(parsed),
        "number_count": number_count(parsed),
        "dot_count": dot_count(parsed),
        "hyphen_count": hyphen_count(parsed),
        "path_depth": path_depth(parsed),
        "has_params": has_params(parsed),
        "entropy": entropy(parsed),
    }
