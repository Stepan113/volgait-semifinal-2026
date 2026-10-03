"""Проверки ввода даты и выбора даты через календарь."""

import allure
import pytest

from pages.calendar_page import CalendarPage


@allure.title("Календарь: поле даты и формат ввода видны")
def test_calendar_form_is_visible(browser):
    page = CalendarPage(browser).open()

    with allure.step("Проверить поле даты и подсказку формата"):
        assert page.date_field().is_displayed()
        assert page.format_hint() == "YYYY-MM-DD"


@allure.title("Календарь: корректную дату можно ввести вручную")
def test_valid_date_can_be_entered(browser):
    page = CalendarPage(browser).open()
    page.enter_date("2026-10-15")

    with allure.step("Проверить введённую дату"):
        assert page.date_value() == "2026-10-15"
        assert not page.is_invalid()


@allure.title("Календарь: выбор дня заполняет поле даты")
def test_day_can_be_selected(browser):
    page = CalendarPage(browser).open()
    page.show_month(2024, 5)
    page.choose_day(15)

    with allure.step("Проверить дату в поле"):
        assert page.date_value() == "2024-05-15"


@allure.title("Календарь: переход к предыдущему месяцу")
def test_previous_month(browser):
    page = CalendarPage(browser).open()
    page.show_month(2024, 3)
    page.previous_month()

    with allure.step("Проверить открытый месяц"):
        assert page.displayed_month() == "February"
        assert page.displayed_year() == "2024"

    page.choose_day(29)
    assert page.date_value() == "2024-02-29"


@allure.title("Календарь: следующий месяц переводит через границу года")
def test_next_month_across_year(browser):
    page = CalendarPage(browser).open()
    page.show_month(2024, 12)
    page.next_month()

    with allure.step("Проверить январь следующего года"):
        assert page.displayed_month() == "January"
        assert page.displayed_year() == "2025"

    page.choose_day(1)
    assert page.date_value() == "2025-01-01"


@allure.title("Календарь: месяц можно выбрать из списка")
def test_month_picker(browser):
    page = CalendarPage(browser).open()
    page.show_month(2024, 1)
    page.select_month(7)

    with allure.step("Проверить выбранный месяц и дату"):
        assert page.displayed_month() == "July"
        page.choose_day(4)
        assert page.date_value() == "2024-07-04"


@allure.title("Календарь: год можно выбрать из списка")
def test_year_picker(browser):
    page = CalendarPage(browser).open()
    page.show_month(2026, 2)
    page.select_year(2024)

    with allure.step("Проверить високосный год и 29 февраля"):
        assert page.displayed_year() == "2024"
        page.choose_day(29)
        assert page.date_value() == "2024-02-29"


@allure.title("Календарь: можно выбрать день соседнего месяца")
def test_adjacent_month_day(browser):
    page = CalendarPage(browser).open()
    page.show_month(2024, 2)
    page.choose_day(1, other_month=True)

    with allure.step("Проверить, что выбран первый день марта"):
        assert page.date_value() == "2024-03-01"


@allure.title("Календарь: отправка корректной даты показывает подтверждение")
def test_valid_date_submission(browser):
    page = CalendarPage(browser).open()
    page.enter_date("2024-02-29")
    page.submit()

    with allure.step("Проверить подтверждение и отправленную дату"):
        success = page.success_text()
        assert "Thank you for your response." in success
        assert "2024-02-29" in success


@pytest.mark.parametrize(
    "value, reason",
    [
        pytest.param("2026/10/15", "неверный разделитель", id="wrong-format"),
        pytest.param("2026-13-01", "несуществующий месяц", id="invalid-month"),
        pytest.param("2026-02-30", "несуществующий день", id="invalid-day"),
        pytest.param("2025-02-29", "29 февраля в невисокосном году", id="non-leap-year"),
    ],
)
@allure.title("Календарь: неверная дата — {reason}")
def test_invalid_date_is_rejected(browser, value, reason):
    page = CalendarPage(browser).open()
    page.enter_date(value)

    with allure.step("Проверить сообщение об ошибке"):
        assert page.is_invalid()
        assert page.validation_message() == "Please enter a valid date."

    page.submit()
    with allure.step("Проверить, что подтверждение не показано"):
        assert page.is_invalid()
        assert not page.success_is_visible()
