from baby_steps import then, when

from vedro_pyppeteer import PyppeteerPlugin


def test_plugin():
    with when:
        plugin = PyppeteerPlugin()

    with then:
        assert isinstance(plugin, PyppeteerPlugin)
