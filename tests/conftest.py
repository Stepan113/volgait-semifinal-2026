from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # Allure создаёт папку относительно текущего каталога запуска.
    # Привязываем её к корню проекта, в том числе при запуске из PyCharm.
    if config.option.allure_report_dir:
        report_dir = Path(config.option.allure_report_dir)
        if not report_dir.is_absolute():
            config.option.allure_report_dir = str(config.rootpath / report_dir)


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    # Ubuntu Snap: используем уже установленные Chromium и ChromeDriver.
    # Иначе Selenium Manager может долго искать и скачивать браузер.
    snap_path = Path("/snap/chromium/current/usr/lib/chromium-browser")
    if (snap_path / "chrome").exists() and (snap_path / "chromedriver").exists():
        options.binary_location = str(snap_path / "chrome")
        driver = webdriver.Chrome(
            service=Service(str(snap_path / "chromedriver")), options=options
        )
    else:
        driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
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
