from pathlib import Path

import pytest
from baby_steps import given, then, when

from vedro_playwright._screenshot_path import ScreenshotPath


@pytest.fixture()
def dir_path():
    return Path("screenshots")


def test_screenshot_path(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / "screenshot.png"


def test_screenshot_path_with_scenario_path(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)
        path.scenario_path = Path("scenarios/scenario1.py").resolve()

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / "scenarios/scenario1/screenshot.png"


def test_screenshot_path_with_scenario_subject(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)
        path.scenario_subject = "<subject>"

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / "<subject>.png"


def test_screenshot_path_with_rerun(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)
        path.rerun = 1

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / f"[{path.rerun}]screenshot.png"


def test_screenshot_path_with_timestamp(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)
        path.timestamp = 1234

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / f"screenshot__{path.timestamp}.png"


def test_screenshot_path_with_step_name(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)
        path.step_name = "<step>"

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / f"screenshot__{path.step_name}.png"


def test_screenshot_path_with_tab_index(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)
        path.tab_index = 1

    with when:
        resolved = path.resolve()

    with then:
        assert resolved == dir_path / f"tab{path.tab_index}__screenshot.png"


def test_screenshot_path_repr(*, dir_path: Path):
    with given:
        path = ScreenshotPath(dir_path)

    with when:
        res = repr(path)

    with then:
        assert res == "ScreenshotPath<screenshots/screenshot.png>"
