from pathlib import Path
from shutil import rmtree
from time import time
from typing import Any, Dict, List, Optional, Tuple, Union

import vedro
from pyppeteer.browser import Browser
from pyppeteer.launcher import Launcher
from pyppeteer.page import Page
from vedro.core import Dispatcher, Plugin
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
    ScenarioFailedEvent,
    ScenarioRunEvent,
    StartupEvent,
    StepFailedEvent,
    StepPassedEvent,
)

from ._browser_context import BrowserContext
from ._screenshot_path import ScreenshotPath

__all__ = ("PyppeteerPlugin", "opened_browser", "opened_browser_page",)

_browser_ctx = BrowserContext()


@vedro.context
async def opened_browser(options: Optional[Dict[str, Any]] = None) -> Browser:
    if options is None:
        options = {"headless": True}
    options = {**options, "autoClose": False}

    launcher = Launcher(options)
    browser = await launcher.launch()
    _browser_ctx.set(browser)

    vedro.defer(browser.close)
    vedro.defer(_browser_ctx.clear)

    return browser


@vedro.context
async def opened_browser_page(browser: Optional[Browser] = None) -> Page:
    if browser is None:
        browser = await opened_browser()

    pages = await browser.pages()
    page = pages[0]
    return page


class PyppeteerPlugin(Plugin):
    def __init__(self, browser_ctx: BrowserContext = _browser_ctx) -> None:
        super().__init__()
        self._browser_ctx = browser_ctx
        self._enabled = False
        self._dir = Path("./screenshots")
        self._only_failed = False
        self._buffer: List[Tuple[bytes, Path]] = []

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(StartupEvent, self.on_startup) \
                  .listen(ScenarioRunEvent, self.on_scenario_run) \
                  .listen(ScenarioFailedEvent, self.on_scenario_failed) \
                  .listen(StepPassedEvent, self.on_step_end) \
                  .listen(StepFailedEvent, self.on_step_end)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        event.arg_parser.add_argument("--pyppeteer-screenshots",
                                      action="store_true",
                                      default=self._enabled,
                                      help="Enable pyppeteer screenshots")
        help_message = f"Set directory for pyppeteer screenshots (default: {self._dir})"
        event.arg_parser.add_argument("--pyppeteer-screenshots-dir",
                                      default=self._dir,
                                      help=help_message)
        event.arg_parser.add_argument("--pyppeteer-screenshots-only-failed",
                                      action="store_true",
                                      default=self._only_failed,
                                      help="Save screenshots only for failed scenarios")

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._enabled = event.args.pyppeteer_screenshots
        self._dir = Path(event.args.pyppeteer_screenshots_dir).resolve()
        self._only_failed = event.args.pyppeteer_screenshots_only_failed
        self._reruns = event.args.reruns

    def on_startup(self, event: StartupEvent) -> None:
        if self._enabled and self._dir.exists():
            rmtree(self._dir)

    def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        if not self._enabled:
            return
        self._path = ScreenshotPath(self._dir)
        self._path.scenario_path = event.scenario_result.scenario.path
        self._path.scenario_subject = event.scenario_result.scenario.subject
        if self._reruns > 0:
            self._path.rerun = event.scenario_result.rerun
        self._buffer = []

    def _save_screenshot(self, screenshot: bytes, path: Path) -> None:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.write_bytes(screenshot)

    async def on_step_end(self, event: Union[StepPassedEvent, StepFailedEvent]) -> None:
        if not self._enabled:
            return

        browser = self._browser_ctx.get()
        if browser is None:
            return

        pages = await browser.pages()
        for index, page in enumerate(pages):
            self._path.timestamp = int(time() * 1000)
            self._path.step_name = event.step_result.step_name
            if len(pages) > 1:
                self._path.tab_index = index

            path = self._path.resolve()
            screenshot = await page.screenshot()
            if self._only_failed:
                self._buffer.append((screenshot, path))
            else:
                self._save_screenshot(screenshot, path)

    async def on_scenario_failed(self, event: ScenarioFailedEvent) -> None:
        while len(self._buffer) > 0:
            screenshot, path = self._buffer.pop(0)
            self._save_screenshot(screenshot, path)
