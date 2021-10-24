from typing import Union

from pyppeteer.browser import Browser

__all__ = ("BrowserContext",)


class BrowserContext:
    def __init__(self) -> None:
        self._browser: Union[Browser, None] = None

    def set(self, browser: Browser) -> None:
        self._browser = browser

    def get(self) -> Union[Browser, None]:
        return self._browser

    def clear(self) -> None:
        self._browser = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<{self._browser!r}>"
