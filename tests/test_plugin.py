from baby_steps import then, when

from vedro_playwright import Playwright, PlaywrightPlugin


def test_plugin():
    with when:
        plugin = PlaywrightPlugin(Playwright)

    with then:
        assert isinstance(plugin, PlaywrightPlugin)
