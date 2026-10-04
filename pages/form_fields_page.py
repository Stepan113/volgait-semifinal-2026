"""Получение списка инструментов со страницы Form Fields."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class FormFieldsPage:
    URL = "https://practice-automation.com/form-fields/"
    TOOLS = (
        By.XPATH,
        "//form[@id='feedbackForm']/label[normalize-space()='Automation tools']/following-sibling::ul[1]/li",
    )

    def __init__(self, browser):
        self.browser = browser

    @allure.step("Открыть Form Fields и прочитать список Automation tools")
    def automation_tools(self):
        self.browser.get(self.URL)
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.TOOLS)
        )
        return [element.text for element in self.browser.find_elements(*self.TOOLS)]
