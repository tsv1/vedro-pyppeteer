# Vedro Pyppeteer Plugin

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/vedro-pyppeteer/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/vedro-pyppeteer)
[![PyPI](https://img.shields.io/pypi/v/vedro-pyppeteer.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-pyppeteer/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-pyppeteer?style=flat-square)](https://pypi.python.org/pypi/vedro-pyppeteer/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-pyppeteer.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-pyppeteer/)

[Vedro](https://github.com/nikitanovosibirsk/vedro) + [pyppeteer](https://github.com/pyppeteer/pyppeteer)

## Installation

```shell
$ pip3 install vedro-pyppeteer
```

```python
# ./bootstrap.py
import vedro
from vedro_pyppeteer import PyppeteerPlugin

vedro.run(plugins=[PyppeteerPlugin()])
```


## Usage

```python
# ./scenarios/reset_password.py
import vedro
from vedro_pyppeteer import opened_browser_page

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
$ python3 bootstrap.py --pyppeteer-screenshots=on_fail
```

## Documentation

`--pyppeteer-screenshots=<mode>`

| Mode        | Description                                        |
| ----------- | -------------------------------------------------- |
| every_step  | Save screenshots for every step                    |
| only_failed | Save screenshots only for failed steps             |
| on_fail     | Save screenshots for all steps when scenario fails |

`--pyppeteer-screenshots-dir` — Set directory for screenshots (default: ./screenshots)
