import hashlib
import hmac

import requests

from app.data.xt_adapter import XTAdapter


class FakeResponse:
    def __init__(self, payload, status_code=200, headers=None):
        self._payload = payload
        self.status_code = status_code
        self.headers = headers or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_xt_v4_signature_includes_algorithm_recvwindow_method_and_path():
    adapter = XTAdapter("app-key", "secret-key")
    timestamp = "1641446237201"

    expected_payload = (
        "validate-algorithms=HmacSHA256"
        "&validate-appkey=app-key"
        "&validate-recvwindow=5000"
        "&validate-timestamp=1641446237201"
        "#GET#/v4/balances"
    )
    expected = hmac.new(
        b"secret-key",
        expected_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    assert adapter._signature("GET", "/v4/balances", timestamp) == expected
    assert adapter._signature("POST", "/v4/balances", timestamp) != expected


def test_xt_v4_signature_uses_query_and_body_in_order():
    adapter = XTAdapter("app-key", "secret-key")
    timestamp = "1641446237201"
    query = "bizType=SPOT"
    body = '{"quantity":2,"price":39000}'

    expected_payload = (
        "validate-algorithms=HmacSHA256"
        "&validate-appkey=app-key"
        "&validate-recvwindow=5000"
        "&validate-timestamp=1641446237201"
        "#POST#/v4/order#bizType=SPOT#{\"quantity\":2,\"price\":39000}"
    )
    expected = hmac.new(
        b"secret-key",
        expected_payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    assert adapter._signature("POST", "/v4/order", timestamp, query, body) == expected


def test_signed_headers_regenerate_timestamp_and_include_required_metadata(monkeypatch):
    adapter = XTAdapter("app-key", "secret-key")
    monkeypatch.setattr(adapter, "_timestamp_ms", lambda: "1234567890")

    headers = adapter._signed_headers("GET", "/v4/balances")

    assert headers["validate-appkey"] == "app-key"
    assert headers["validate-timestamp"] == "1234567890"
    assert headers["validate-recvwindow"] == "5000"
    assert headers["validate-algorithms"] == "HmacSHA256"
    assert headers["validate-signature"] == adapter._signature(
        "GET", "/v4/balances", "1234567890"
    )


def test_request_json_resyncs_once_after_auth_105(monkeypatch):
    adapter = XTAdapter("app-key", "secret-key")
    responses = [
        FakeResponse({"rc": 1, "mc": "AUTH_105"}),
        FakeResponse({"rc": 0, "mc": "SUCCESS", "result": {}}),
    ]
    timestamps = iter(["1000", "2000"])
    seen = []

    monkeypatch.setattr(adapter, "_timestamp_ms", lambda: next(timestamps))
    monkeypatch.setattr(adapter, "_sync_server_time", lambda: seen.append("resynced"))

    def fake_request(method, url, headers=None, data=None, timeout=None):
        seen.append(headers["validate-timestamp"])
        return responses.pop(0)

    monkeypatch.setattr(adapter.session, "request", fake_request)

    payload = adapter._request_json("GET", "/v4/balances", authenticated=True)

    assert payload["rc"] == 0
    assert seen == ["1000", "resynced", "2000"]


def test_request_json_retries_transient_http_failures(monkeypatch):
    adapter = XTAdapter("app-key", "secret-key")
    responses = [
        FakeResponse({"rc": 1, "mc": "FAILURE"}, status_code=503),
        FakeResponse({"rc": 0, "mc": "SUCCESS", "result": {}}),
    ]
    monkeypatch.setattr("app.data.xt_adapter.time.sleep", lambda _: None)
    monkeypatch.setattr(
        adapter.session,
        "request",
        lambda *args, **kwargs: responses.pop(0),
    )

    payload = adapter._request_json("GET", "/v4/public/time")

    assert payload["rc"] == 0
