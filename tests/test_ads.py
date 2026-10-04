"""Позитивные и негативные проверки рекламного окна."""

from time import sleep

import allure
import pytest
from selenium.common.exceptions import ElementClickInterceptedException

from pages.ads_page import AdsPage


@allure.title("Реклама: страница показывает заголовок и описание")
def test_ads_page_content(browser):
    page = AdsPage(browser).open()

    with allure.step("Проверить текст страницы"):
        assert page.heading() == "Ads"
        assert "An ad will appear in 5" in page.page_text()


@allure.title("Реклама: окно появляется автоматически")
def test_ad_opens_automatically(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()

    with allure.step("Проверить видимость рекламы"):
        assert page.ad_is_visible()


@allure.title("Реклама: окно показывает заголовок и текст")
def test_ad_content(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()

    with allure.step("Проверить содержимое рекламы"):
        assert page.ad_title() == "Hi"
        assert page.ad_text() == "I am an ad."


@allure.title("Реклама: кнопка закрытия доступна")
def test_close_button_is_available(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()

    with allure.step("Проверить кнопку ×"):
        assert page.close_button().is_displayed()
        assert page.close_button().is_enabled()


@allure.title("Реклама: кнопка × закрывает окно")
def test_close_button_hides_ad(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()
    page.close_ad()

    with allure.step("Проверить, что реклама скрыта"):
        assert not page.ad_is_visible()


@allure.title("Реклама: после закрытия доступен переход на главную")
def test_page_is_usable_after_closing_ad(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()
    page.close_ad()
    page.go_home()

    with allure.step("Проверить адрес главной страницы"):
        assert browser.current_url == "https://practice-automation.com/"


@allure.title("Реклама: после закрытия окно само не открывается повторно")
def test_ad_stays_closed(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()
    page.close_ad()

    with allure.step("Подождать дольше задержки автопоказа и проверить окно"):
        sleep(6)
        assert not page.ad_is_visible()


@allure.title("Реклама: Escape не закрывает окно")
def test_escape_does_not_close_ad(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()
    page.press_escape()

    with allure.step("Проверить, что реклама осталась открытой"):
        assert page.ad_is_visible()


@allure.title("Реклама: клик по затемнённому фону не закрывает окно")
def test_backdrop_click_does_not_close_ad(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()
    page.click_backdrop()

    with allure.step("Проверить, что реклама осталась открытой"):
        assert page.ad_is_visible()


@allure.title("Реклама: открытое окно блокирует ссылку под ним")
def test_ad_blocks_background_link(browser):
    page = AdsPage(browser).open()
    page.wait_for_ad()

    with allure.step("Попытаться нажать ссылку Home под рекламой"):
        with pytest.raises(ElementClickInterceptedException):
            page.home_link().click()

    with allure.step("Проверить, что перехода не было"):
        assert browser.current_url == AdsPage.URL
