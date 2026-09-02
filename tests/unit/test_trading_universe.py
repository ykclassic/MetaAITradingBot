from app.config import DEFAULT_TRADE_SYMBOLS, AppConfig


def test_default_trading_universe_contains_all_supported_pairs(monkeypatch):
    monkeypatch.delenv("TRADE_SYMBOLS", raising=False)
    config = AppConfig.load_from_env()
    assert config.symbols == [
        "BTC_USDT",
        "ETH_USDT",
        "SOL_USDT",
        "BNB_USDT",
        "XRP_USDT",
        "ADA_USDT",
        "LINK_USDT",
    ]
    assert DEFAULT_TRADE_SYMBOLS.count("_") == 7


def test_explicit_symbol_configuration_is_normalized(monkeypatch):
    monkeypatch.setenv("TRADE_SYMBOLS", " sol_usdt, BNB_USDT ,xrp_usdt ")
    config = AppConfig.load_from_env()
    assert config.symbols == ["SOL_USDT", "BNB_USDT", "XRP_USDT"]
