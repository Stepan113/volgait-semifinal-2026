"""Действия с двумя модальными окнами страницы Modals."""

import allure
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ModalsPage:
    URL = "https://practice-automation.com/modals/"
    SIMPLE = (By.ID, "pum-1318")
    FORM = (By.ID, "pum-674")
    NAME = (By.ID, "g1051-name")
    EMAIL = (By.ID, "g1051-email")
    MESSAGE = (By.ID, "contact-form-comment-g1051-message")
    SUCCESS = (By.CSS_SELECTOR, "#pum-674 .contact-form-submission")

    def __init__(self, browser):
        self.browser = browser

    @allure.step("Открыть страницу Modals")
    def open(self):
        self.browser.get(self.URL)
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.ID, "simpleModal"))
        )
        return self

    @allure.step("Открыть простое модальное окно")
    def open_simple(self):
        self.browser.find_element(By.ID, "simpleModal").click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located(self.SIMPLE))

    @allure.step("Открыть модальное окно с формой")
    def open_form(self):
        self.browser.find_element(By.ID, "formModal").click()
        WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located(self.FORM))

    @allure.step("Закрыть простое окно кнопкой ×")
    def close_simple(self):
        self.browser.find_element(By.CSS_SELECTOR, "#pum-1318 .pum-close").click()
        WebDriverWait(self.browser, 5).until(EC.invisibility_of_element_located(self.SIMPLE))

    @allure.step("Закрыть окно с формой кнопкой ×")
    def close_form(self):
        self.browser.find_element(By.CSS_SELECTOR, "#pum-674 .pum-close").click()
        WebDriverWait(self.browser, 5).until(EC.invisibility_of_element_located(self.FORM))

    @allure.step("Нажать Escape")
    def press_escape(self):
        self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def wait_for_form_to_close(self):
        WebDriverWait(self.browser, 5).until(
            EC.invisibility_of_element_located(self.FORM)
        )

    def simple_is_visible(self):
        return self.browser.find_element(*self.SIMPLE).is_displayed()

    def form_is_visible(self):
        return self.browser.find_element(*self.FORM).is_displayed()

    def simple_title(self):
        return self.browser.find_element(By.ID, "pum_popup_title_1318").get_attribute("textContent").strip()

    def simple_text(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "#pum-1318 .pum-content"
        ).get_attribute("textContent").strip()

    def form_title(self):
        return self.browser.find_element(By.ID, "pum_popup_title_674").get_attribute("textContent").strip()

    def name_field(self):
        return self.browser.find_element(*self.NAME)

    def email_field(self):
        return self.browser.find_element(*self.EMAIL)

    def message_field(self):
        return self.browser.find_element(*self.MESSAGE)

    @allure.step("Заполнить форму: имя, email и сообщение")
    def fill_form(self, name, email, message):
        self.name_field().send_keys(name)
        self.email_field().send_keys(email)
        self.message_field().send_keys(message)

    @allure.step("Отправить форму модального окна")
    def submit_form(self):
        self.browser.find_element(By.CSS_SELECTOR, "#pum-674 button[type='submit']").click()

    def name_error(self):
        selector = (By.ID, "g1051-name-text-error-message")
        WebDriverWait(self.browser, 5).until(
            EC.text_to_be_present_in_element(selector, "This field is required.")
        )
        return self.browser.find_element(*selector).text

    def email_error(self):
        selector = (By.ID, "g1051-email-email-error-message")
        WebDriverWait(self.browser, 5).until(
            EC.text_to_be_present_in_element(selector, "Please enter a valid email address")
        )
        return self.browser.find_element(*selector).text

    def success_text(self):
        WebDriverWait(self.browser, 15).until(
            lambda browser: self.success_is_visible()
        )
        return self.browser.find_element(*self.SUCCESS).text

    def success_is_visible(self):
        message = self.browser.find_element(*self.SUCCESS)
        return message.is_displayed() and message.get_attribute("aria-hidden") != "true"
