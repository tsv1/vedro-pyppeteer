from typing import Any, Dict, Optional, cast

import vedro
from playwright.async_api import Browser, Page

from ._browser_engine import BrowserEngine
from ._vedro_playwright import opened_browser, opened_browser_page

__all__ = ("opened_chromium", "opened_chromium_page",
           "opened_firefox", "opened_firefox_page",
           "opened_webkit", "opened_webkit_page",)


# chromium

@vedro.context
async def opened_chromium(options: Optional[Dict[str, Any]] = None) -> Browser:
    browser = await opened_browser(BrowserEngine.CHROMIUM, options)
    return cast(Browser, browser)


@vedro.context
async def opened_chromium_page(browser: Optional[Browser] = None) -> Page:
    if browser is None:
        browser = await opened_chromium()
    page = await opened_browser_page(browser)
    return cast(Page, page)


# firefox

@vedro.context
async def opened_firefox(options: Optional[Dict[str, Any]] = None) -> Browser:
    browser = await opened_browser(BrowserEngine.FIREFOX, options)
    return cast(Browser, browser)


@vedro.context
async def opened_firefox_page(browser: Optional[Browser] = None) -> Page:
    if browser is None:
        browser = await opened_firefox()
    page = await opened_browser_page(browser)
    return cast(Page, page)


# webkit

@vedro.context
async def opened_webkit(options: Optional[Dict[str, Any]] = None) -> Browser:
    browser = await opened_browser(BrowserEngine.WEBKIT, options)
    return cast(Browser, browser)


@vedro.context
async def opened_webkit_page(browser: Optional[Browser] = None) -> Page:
    if browser is None:
        browser = await opened_webkit()
    page = await opened_browser_page(browser)
    return cast(Page, page)
