"""Действия с формой и календарём на странице Calendars."""

import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CalendarPage:
    URL = "https://practice-automation.com/calendars/"
    DATE_FIELD = (By.CSS_SELECTOR, "form[aria-label='Calendars'] input.jp-contact-form-date")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "form[aria-label='Calendars'] button[type='submit']")
    SUCCESS_MESSAGE = (
        By.CSS_SELECTOR,
        ".jetpack-contact-form-container.is-single-input-form .contact-form-submission",
    )
    DATE_ERROR = (By.CSS_SELECTOR, "form[aria-label='Calendars'] .contact-form__input-error.has-errors")

    def __init__(self, browser):
        self.browser = browser

    @allure.step("Открыть страницу Calendars")
    def open(self):
        self.browser.get(self.URL)
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located(self.DATE_FIELD)
        )
        return self

    def date_field(self):
        return self.browser.find_element(*self.DATE_FIELD)

    def date_value(self):
        return self.date_field().get_attribute("value")

    def format_hint(self):
        return self.browser.find_element(
            By.CSS_SELECTOR, "form[aria-label='Calendars'] .contact-form__field-format"
        ).text

    @allure.step("Ввести дату {value} в поле")
    def enter_date(self, value):
        field = self.date_field()
        field.clear()
        field.send_keys(value)
        # Уводим фокус, чтобы сайт проверил введённую дату.
        self.browser.find_element(By.TAG_NAME, "h1").click()

    def is_invalid(self):
        return self.date_field().get_attribute("aria-invalid") == "true"

    def validation_message(self):
        error = WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located(self.DATE_ERROR)
        )
        return error.text

    @allure.step("Открыть календарь")
    def open_picker(self):
        self.date_field().click()
        WebDriverWait(self.browser, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dp-cal"))
        )

    def displayed_month(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".dp-cal-month").text

    def displayed_year(self):
        return self.browser.find_element(By.CSS_SELECTOR, ".dp-cal-year").text

    @allure.step("Выбрать год {year} в календаре")
    def select_year(self, year):
        self.browser.find_element(By.CSS_SELECTOR, ".dp-cal-year").click()
        self.browser.find_element(By.CSS_SELECTOR, f".dp-year[data-year='{year}']").click()

    @allure.step("Выбрать месяц {month} в календаре")
    def select_month(self, month):
        self.browser.find_element(By.CSS_SELECTOR, ".dp-cal-month").click()
        self.browser.find_element(
            By.CSS_SELECTOR, f".dp-month[data-month='{month - 1}']"
        ).click()

    def show_month(self, year, month):
        """Открыть заданный месяц, чтобы тесты не зависели от текущей даты."""
        self.open_picker()
        self.select_year(year)
        self.select_month(month)

    @allure.step("Перейти к предыдущему месяцу")
    def previous_month(self):
        self.browser.find_element(By.CSS_SELECTOR, ".dp-prev").click()

    @allure.step("Перейти к следующему месяцу")
    def next_month(self):
        self.browser.find_element(By.CSS_SELECTOR, ".dp-next").click()

    @allure.step("Выбрать день {day} в календаре")
    def choose_day(self, day, other_month=False):
        selector = ".dp-day.dp-edge-day" if other_month else ".dp-day:not(.dp-edge-day)"
        for button in self.browser.find_elements(By.CSS_SELECTOR, selector):
            if button.text == str(day):
                button.click()
                return
        raise NoSuchElementException(f"День {day} не найден в календаре")

    @allure.step("Отправить форму с датой")
    def submit(self):
        self.browser.find_element(*self.SUBMIT_BUTTON).click()

    def success_text(self):
        message = WebDriverWait(self.browser, 15).until(
            EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
        )
        return message.text

    def success_is_visible(self):
        return self.browser.find_element(*self.SUCCESS_MESSAGE).is_displayed()
