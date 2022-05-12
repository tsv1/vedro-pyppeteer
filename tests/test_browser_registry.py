from unittest.mock import Mock

from baby_steps import given, then, when

from vedro_playwright._browser_registry import BrowserRegistry


def test_browser_context_get():
    with given:
        browser_registry = BrowserRegistry()

    with when:
        res = browser_registry.get()

    with then:
        assert res is None


def test_browser_context_set():
    with given:
        browser_registry = BrowserRegistry()
        browser = Mock()

    with when:
        res = browser_registry.set(browser)

    with then:
        assert res is None


def test_browser_context_get_setted():
    with given:
        browser_registry = BrowserRegistry()
        browser = Mock()
        browser_registry.set(browser)

    with when:
        res = browser_registry.get()

    with then:
        assert res == browser


def test_browser_context_clear():
    with given:
        browser_registry = BrowserRegistry()

    with when:
        res = browser_registry.clear()

    with then:
        assert res is None


def test_browser_context_get_cleared():
    with given:
        browser_registry = BrowserRegistry()
        browser = Mock()
        browser_registry.set(browser)
        browser_registry.clear()

    with when:
        res = browser_registry.get()

    with then:
        assert res is None


def test_browser_context_repr():
    with given:
        browser_registry = BrowserRegistry()

    with when:
        res = repr(browser_registry)

    with then:
        assert res == "BrowserRegistry<None>"


def test_browser_context_repr_setted():
    with given:
        browser_registry = BrowserRegistry()
        browser = Mock()
        browser_registry.set(browser)

    with when:
        res = repr(browser_registry)

    with then:
        assert res == f"BrowserRegistry<{browser}>"
