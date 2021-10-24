from pathlib import Path
from shutil import rmtree
from time import time
from typing import Any, Dict, Optional, Union

import vedro
from pyppeteer.browser import Browser
from pyppeteer.launcher import Launcher
from pyppeteer.page import Page
from vedro.core import Dispatcher, Plugin, ScenarioResult
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
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
async def opened_browser_page(browser: Optional[Browser]) -> Page:
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
        self._scenario_result: Union[ScenarioResult, None] = None

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(ArgParseEvent, self.on_arg_parse) \
                  .listen(ArgParsedEvent, self.on_arg_parsed) \
                  .listen(StartupEvent, self.on_startup) \
                  .listen(ScenarioRunEvent, self.on_scenario_run) \
                  .listen(StepPassedEvent, self.on_step_end) \
                  .listen(StepFailedEvent, self.on_step_end)

    def on_arg_parse(self, event: ArgParseEvent) -> None:
        event.arg_parser.add_argument("--pyppeteer-sreenshots",
                                      action="store_true",
                                      default=self._enabled,
                                      help="Enable pyppeteer screenshots")
        help_message = f"Set directory for pyppeteer screenshots (default: {self._dir})"
        event.arg_parser.add_argument("--pyppeteer-sreenshots-dir",
                                      default=self._dir,
                                      help=help_message)

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._enabled = event.args.pyppeteer_sreenshots
        self._dir = Path(event.args.pyppeteer_sreenshots_dir).resolve()
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

    async def on_step_end(self, event: Union[StepPassedEvent, StepFailedEvent]) -> None:
        if not self._enabled:
            return

        browser = self._browser_ctx.get()
        if browser is None:
            return

        screenshot_path = self._path.resolve()
        if not screenshot_path.parent.exists():
            screenshot_path.parent.mkdir(parents=True)

        pages = await browser.pages()
        for index, page in enumerate(pages):
            self._path.timestamp = int(time() * 1000)
            self._path.step_name = event.step_result.step_name
            if len(pages) > 1:
                self._path.tab_index = index
            await page.screenshot({"path": self._path.resolve()})
