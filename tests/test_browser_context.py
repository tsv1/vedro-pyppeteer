from unittest.mock import Mock

from baby_steps import given, then, when

from vedro_pyppeteer._browser_context import BrowserContext


def test_browser_context_get():
    with given:
        browser_ctx = BrowserContext()

    with when:
        res = browser_ctx.get()

    with then:
        assert res is None


def test_browser_context_set():
    with given:
        browser_ctx = BrowserContext()
        browser = Mock()

    with when:
        res = browser_ctx.set(browser)

    with then:
        assert res is None


def test_browser_context_get_setted():
    with given:
        browser_ctx = BrowserContext()
        browser = Mock()
        browser_ctx.set(browser)

    with when:
        res = browser_ctx.get()

    with then:
        assert res == browser


def test_browser_context_clear():
    with given:
        browser_ctx = BrowserContext()

    with when:
        res = browser_ctx.clear()

    with then:
        assert res is None


def test_browser_context_get_cleared():
    with given:
        browser_ctx = BrowserContext()
        browser = Mock()
        browser_ctx.set(browser)
        browser_ctx.clear()

    with when:
        res = browser_ctx.get()

    with then:
        assert res is None


def test_browser_context_repr():
    with given:
        browser_ctx = BrowserContext()

    with when:
        res = repr(browser_ctx)

    with then:
        assert res == "BrowserContext<None>"


def test_browser_context_repr_setted():
    with given:
        browser_ctx = BrowserContext()
        browser = Mock()
        browser_ctx.set(browser)

    with when:
        res = repr(browser_ctx)

    with then:
        assert res == f"BrowserContext<{browser}>"
