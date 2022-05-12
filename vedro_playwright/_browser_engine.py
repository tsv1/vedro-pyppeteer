from enum import Enum

__all__ = ("BrowserEngine",)


class BrowserEngine(Enum):
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"

    def __str__(self) -> str:
        return self.value
