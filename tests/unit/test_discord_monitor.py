from app.monitor.discord import DiscordSystemMonitor


def test_monitor_disabled_does_not_send(monkeypatch):
    called = False

    def fail_post(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("disabled monitor must not send")

    monkeypatch.setattr("app.monitor.discord.requests.post", fail_post)
    monitor = DiscordSystemMonitor("")
    monitor.cycle_started(["BTC_USDT"], "M15")
    assert called is False


def test_monitor_delivery_failure_is_non_fatal(monkeypatch):
    def fail_post(*args, **kwargs):
        raise RuntimeError("network failure")

    monkeypatch.setattr("app.monitor.discord.requests.post", fail_post)
    monitor = DiscordSystemMonitor("https://discord.example/webhook")
    # RuntimeError is intentionally outside requests.RequestException; ensure
    # this test documents that only requests transport failures are expected.
    # Replace with a requests-compatible exception below.
    import requests
    def fail_requests_post(*args, **kwargs):
        raise requests.RequestException("network failure")
    monkeypatch.setattr("app.monitor.discord.requests.post", fail_requests_post)
    monitor.error("TEST", "monitor failure must not escape")
