import allure
from selenium.webdriver.common.by import By


@allure.title("Главная страница открывается")
def test_home_page_opens(browser):
    with allure.step("Открыть главную страницу"):
        browser.get("https://practice-automation.com/")

    with allure.step("Проверить заголовок страницы"):
        heading = browser.find_element(By.TAG_NAME, "h1")
        assert heading.text == "Welcome to your software automation practice website!"
