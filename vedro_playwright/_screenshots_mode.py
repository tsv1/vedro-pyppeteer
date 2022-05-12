from enum import Enum

__all__ = ("ScreenshotsMode",)


class ScreenshotsMode(Enum):
    EVERY_STEP = "every_step"
    ONLY_FAILED = "only_failed"
    ON_FAIL = "on_fail"
    DISABLED = "disabled"

    def __str__(self) -> str:
        return self.value
