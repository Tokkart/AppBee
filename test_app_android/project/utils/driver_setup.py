from appium import webdriver
from appium.options.android import UiAutomator2Options

def setup_driver():
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        appPackage='ru.beeline.services',
        appActivity='ru.beeline.activity.MainActivity',
        language='ru',
        locale='RU'
)
    appium_server_url = 'http://localhost:4723'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
    return driver