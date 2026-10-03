import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("browser")
        if browser is not None:
            try:
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="Скриншот при ошибке",
                    attachment_type=allure.attachment_type.PNG,
                )
            except WebDriverException:
                pass
