# Vedro Playwright Plugin

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/vedro-playwright/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/vedro-playwright)
[![PyPI](https://img.shields.io/pypi/v/vedro-playwright.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-playwright/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-playwright?style=flat-square)](https://pypi.python.org/pypi/vedro-playwright/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-playwright.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-playwright/)

[Vedro](https://github.com/nikitanovosibirsk/vedro) + [playwright](https://playwright.dev/python/)

## Installation

### 1. Install package

```shell
$ pip3 install vedro-playwright
```

### 2. Enable plugin

```python
# ./vedro.cfg.py
import vedro
import vedro_playwright as playwright

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class Playwright(playwright.Playwright):
            enabled = True
```

## Usage

```python
# ./scenarios/reset_password.py
import vedro
from vedro_playwright import opened_browser_page

class Scenario(vedro.Scenario):
    subject = "reset password"

    async def given_opened_app(self):
        self.page = await opened_browser_page()
        await self.page.goto("http://localhost/reset")

    async def given_filled_email(self):
        form_email = await self.page.querySelector("#form-email")
        await form_email.type("user@email")

    async def when_user_submits_form(self):
        await self.page.click("#form-submit")

    async def then_it_should_redirect_to_root_page(self):
        pathname = await self.page.evaluate("window.location.pathname")
        assert pathname == "/"
```

```shell
$ vedro run --playwright-screenshots=on_fail
```

## Documentation

`--playwright-screenshots=<mode>`

| Mode        | Description                                        |
| ----------- | -------------------------------------------------- |
| every_step  | Save screenshots for every step                    |
| only_failed | Save screenshots only for failed steps             |
| on_fail     | Save screenshots for all steps when scenario fails |

`--playwright-screenshots-dir` — Set directory for screenshots (default: ./screenshots)
