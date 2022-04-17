from baby_steps import then, when

from vedro_pyppeteer import PyppeteerPlugin, Pyppeteer


def test_plugin():
    with when:
        plugin = PyppeteerPlugin(Pyppeteer)

    with then:
        assert isinstance(plugin, PyppeteerPlugin)
