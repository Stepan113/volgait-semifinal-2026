"""Позитивные и негативные проверки модальных окон."""

import allure

from pages.form_fields_page import FormFieldsPage
from pages.modals_page import ModalsPage


@allure.title("Модальные окна: простое окно показывает заголовок и текст")
def test_simple_modal_content(browser):
    page = ModalsPage(browser).open()
    page.open_simple()

    with allure.step("Проверить содержимое окна"):
        assert page.simple_title() == "Simple Modal"
        assert "Hi, I’m a simple modal." in page.simple_text()


@allure.title("Модальные окна: простое окно закрывается кнопкой ×")
def test_simple_modal_closes(browser):
    page = ModalsPage(browser).open()
    page.open_simple()
    page.close_simple()

    with allure.step("Проверить, что окно скрыто"):
        assert not page.simple_is_visible()


@allure.title("Модальные окна: простое окно можно открыть повторно")
def test_simple_modal_reopens(browser):
    page = ModalsPage(browser).open()
    page.open_simple()
    page.close_simple()
    page.open_simple()

    with allure.step("Проверить повторное открытие"):
        assert page.simple_is_visible()


@allure.title("Модальные окна: форма показывает поля и кнопку отправки")
def test_form_modal_fields(browser):
    page = ModalsPage(browser).open()
    page.open_form()

    with allure.step("Проверить заголовок и поля"):
        assert page.form_title() == "Modal Containing A Form"
        assert page.name_field().is_displayed()
        assert page.email_field().is_displayed()
        assert page.message_field().is_displayed()
        assert page.name_field().get_attribute("required") is not None


@allure.title("Модальные окна: форму можно закрыть кнопкой ×")
def test_form_modal_closes(browser):
    page = ModalsPage(browser).open()
    page.open_form()
    page.close_form()

    with allure.step("Проверить, что форма скрыта"):
        assert not page.form_is_visible()


@allure.title("Модальные окна: форму можно закрыть клавишей Escape")
def test_form_modal_closes_with_escape(browser):
    page = ModalsPage(browser).open()
    page.open_form()
    page.press_escape()
    page.wait_for_form_to_close()

    with allure.step("Проверить, что форма скрыта"):
        assert not page.form_is_visible()


@allure.title("Модальные окна: Message заполняется списком Automation tools")
def test_message_contains_automation_tools(browser):
    tools = FormFieldsPage(browser).automation_tools()
    assert tools, "Список Automation tools пуст"
    message = ", ".join(tools)

    page = ModalsPage(browser).open()
    page.open_form()
    page.fill_form("Test User", "test@example.com", message)

    with allure.step("Проверить текст, полученный со страницы Form Fields"):
        assert page.message_field().get_attribute("value") == message
        assert page.name_field().get_attribute("value") == "Test User"
        assert page.email_field().get_attribute("value") == "test@example.com"


@allure.title("Модальные окна: корректная форма показывает подтверждение")
def test_form_submission(browser):
    tools = FormFieldsPage(browser).automation_tools()
    assert tools, "Список Automation tools пуст"

    page = ModalsPage(browser).open()
    page.open_form()
    page.fill_form("Test User", "test@example.com", ", ".join(tools))
    page.submit_form()

    with allure.step("Проверить подтверждение отправки"):
        assert "Thank you for your response." in page.success_text()


@allure.title("Модальные окна: Escape не закрывает простое окно")
def test_simple_modal_ignores_escape(browser):
    page = ModalsPage(browser).open()
    page.open_simple()
    page.press_escape()

    with allure.step("Проверить, что окно осталось открытым"):
        assert page.simple_is_visible()


@allure.title("Модальные окна: пустое обязательное имя не принимается")
def test_empty_name_is_rejected(browser):
    page = ModalsPage(browser).open()
    page.open_form()
    page.submit_form()

    with allure.step("Проверить ошибку имени и отсутствие подтверждения"):
        assert page.name_error() == "This field is required."
        assert not page.success_is_visible()


@allure.title("Модальные окна: неверный email не принимается")
def test_invalid_email_is_rejected(browser):
    page = ModalsPage(browser).open()
    page.open_form()
    page.fill_form("Test User", "wrong-email", "Test message")
    page.submit_form()

    with allure.step("Проверить ошибку email и отсутствие подтверждения"):
        assert page.email_error() == "Please enter a valid email address"
        assert not page.success_is_visible()
