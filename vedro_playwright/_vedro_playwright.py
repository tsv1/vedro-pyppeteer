from pathlib import Path
from shutil import rmtree
from time import time
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import vedro
from playwright.async_api import Browser, BrowserContext, Page, async_playwright
from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import (
    ArgParsedEvent,
    ArgParseEvent,
    ScenarioFailedEvent,
    ScenarioRunEvent,
    StartupEvent,
    StepFailedEvent,
    StepPassedEvent,
)

from ._browser_engine import BrowserEngine
from ._browser_registry import BrowserRegistry
from ._screenshot_path import ScreenshotPath
from ._screenshots_mode import ScreenshotsMode

__all__ = ("Playwright", "PlaywrightPlugin", "opened_browser", "opened_browser_page",)

_browser_registry = BrowserRegistry()


@vedro.context
async def opened_browser(engine: BrowserEngine = BrowserEngine.CHROMIUM,
                         options: Optional[Dict[str, Any]] = None) -> Browser:
    if options is None:
        options = {"headless": True}

    cm = async_playwright()
    playwright = await cm.__aenter__()
    vedro.defer(cm.__aexit__)

    browser_type = getattr(playwright, engine.value)
    browser: Browser = await browser_type.launch(**options)
    vedro.defer(browser.close)

    _browser_registry.set(browser)
    vedro.defer(_browser_registry.clear)

    return browser


@vedro.context
async def opened_browser_page(browser: Optional[Browser] = None) -> Page:
    if browser is None:
        browser = await opened_browser()

    context: BrowserContext = await browser.new_context()
    # context available via page.context
    page = await context.new_page()
    return page


class PlaywrightPlugin(Plugin):
    def __init__(self, config: Type["Playwright"], *,
                 browser_registry: BrowserRegistry = _browser_registry) -> None:
        super().__init__(config)
        self._browser_registry = browser_registry
        self._mode = ScreenshotsMode.DISABLED
        self._dir = Path()
        self._reruns = 0
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
        group = event.arg_parser.add_argument_group("Playwright")

        group.add_argument("--playwright-screenshots",
                           type=ScreenshotsMode,
                           choices=list(ScreenshotsMode),
                           help="Enable screenshots")

        default_dir = "./screenshots"
        help_message = f"Set directory for screenshots (default: '{default_dir}')"
        group.add_argument("--playwright-screenshots-dir",
                           default=default_dir, help=help_message)

    def on_arg_parsed(self, event: ArgParsedEvent) -> None:
        self._mode = event.args.playwright_screenshots
        self._dir = Path(event.args.playwright_screenshots_dir).resolve()
        self._reruns = event.args.reruns

    def on_startup(self, event: StartupEvent) -> None:
        if self._mode != ScreenshotsMode.DISABLED and self._dir.exists():
            rmtree(self._dir)

    def on_scenario_run(self, event: ScenarioRunEvent) -> None:
        if self._mode == ScreenshotsMode.DISABLED:
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
        if self._mode == ScreenshotsMode.DISABLED:
            return

        browser = self._browser_registry.get()
        if browser is None:
            return

        for context_idx, context in enumerate(browser.contexts):
            for page_idx, page in enumerate(context.pages):
                self._path.timestamp = int(time() * 1000)
                self._path.step_name = event.step_result.step_name
                if len(browser.contexts) > 1:
                    self._path.context_index = context_idx
                if len(context.pages) > 1:
                    self._path.tab_index = page_idx

                path = self._path.resolve()
                screenshot = await page.screenshot()
                if self._mode == ScreenshotsMode.EVERY_STEP:
                    self._save_screenshot(screenshot, path)
                elif self._mode == ScreenshotsMode.ON_FAIL:
                    self._buffer.append((screenshot, path))
                elif (self._mode == ScreenshotsMode.ONLY_FAILED) and event.step_result.is_failed():
                    self._save_screenshot(screenshot, path)

    async def on_scenario_failed(self, event: ScenarioFailedEvent) -> None:
        while len(self._buffer) > 0:
            screenshot, path = self._buffer.pop(0)
            self._save_screenshot(screenshot, path)


class Playwright(PluginConfig):
    plugin = PlaywrightPlugin
