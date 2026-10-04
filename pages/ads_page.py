"""Действия с рекламным окном на странице Ads."""

import allure
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AdsPage:
    URL = "https://practice-automation.com/ads/"
    AD = (By.ID, "pum-1272")
    CLOSE = (By.CSS_SELECTOR, "#pum-1272 .pum-close")
    HOME = (By.CSS_SELECTOR, ".breadcrumbs a")

    def __init__(self, browser):
        self.browser = browser

    @allure.step("Открыть страницу Ads")
    def open(self):
        self.browser.get(self.URL)
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )
        return self

    def heading(self):
        return self.browser.find_element(By.TAG_NAME, "h1").text

    def page_text(self):
        return self.browser.find_element(By.ID, "post-1274").text

    @allure.step("Дождаться автоматического появления рекламы")
    def wait_for_ad(self):
        WebDriverWait(self.browser, 12).until(
            EC.visibility_of_element_located(self.AD)
        )

    def ad_is_visible(self):
        return self.browser.find_element(*self.AD).is_displayed()

    def ad_title(self):
        return self.browser.find_element(
            By.ID, "pum_popup_title_1272"
        ).get_attribute("textContent").strip()

    def ad_text(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "#pum-1272 .pum-content"
        ).get_attribute("textContent").strip()

    def close_button(self):
        # Окно может появиться чуть раньше кнопки закрытия.
        return WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable(self.CLOSE)
        )

    @allure.step("Закрыть рекламу кнопкой ×")
    def close_ad(self):
        self.close_button().click()
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located(self.AD)
        )

    @allure.step("Нажать Escape")
    def press_escape(self):
        self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    @allure.step("Нажать на затемнённый фон рекламы")
    def click_backdrop(self):
        overlay = self.browser.find_element(*self.AD)
        ActionChains(self.browser).move_to_element_with_offset(
            overlay,
            -overlay.size["width"] // 2 + 20,
            -overlay.size["height"] // 2 + 20,
        ).click().perform()

    def home_link(self):
        return self.browser.find_element(*self.HOME)

    @allure.step("Перейти на главную страницу после закрытия рекламы")
    def go_home(self):
        self.home_link().click()
        WebDriverWait(self.browser, 10).until(
            EC.url_to_be("https://practice-automation.com/")
        )
