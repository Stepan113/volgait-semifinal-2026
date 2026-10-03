# Лабораторная работа 1 — автоматизация тестирования

Учебный проект для проверки сайта https://practice-automation.com/ с помощью PyTest и Selenium.

## Текущий тестовый сценарий

**Главная страница открывается**

1. Открыть главную страницу сайта.
2. Проверить, что на странице виден заголовок «Welcome to your software automation practice website!».

Ожидаемый результат: главная страница загрузилась и содержит указанный заголовок.

## Запуск

Нужны Python 3.12+ и установленный Google Chrome.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

Тест запускает Chrome в фоновом режиме. Результаты Allure сохраняются в `allure-results/`. При ошибке теста к результату прикладывается скриншот страницы.

Для просмотра отчёта дополнительно установите Allure CLI и запустите:

```bash
allure serve allure-results
```

Следующий этап работы — описать и автоматизировать сценарии для страниц Calendars, Modals и Ads из задания.
