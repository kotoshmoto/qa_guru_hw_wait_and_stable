import pytest
from selenium.webdriver.common.by import By

from generators.login_form_fields_g import g_get_valid_params, g_get_invalid_params
from helpers.login_form_h import get_result_message

# Локаторы элементов формы на странице
EMAIL_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
LOGIN_BUTTON = (By.ID, "submit-button")
# Селекторы сообщений об ошибке или успехе зависят от верстки страницы QA.GURU
STATUS_MESSAGE = (By.ID, "error-message")


def field_fills(driver, email, password):
    """Функция заполнения полей """

    # 1. Открытие тестируемой страницы
    driver.get("https://qa-guru.github.io/one-page-form/login.html")

    # 2. Поиск элементов формы
    email_field = driver.find_element(*EMAIL_INPUT)
    password_field = driver.find_element(*PASSWORD_INPUT)
    submit_button = driver.find_element(*LOGIN_BUTTON)

    # 3. Очистка полей и ввод тестовых данных
    email_field.clear()
    email_field.send_keys(email)

    password_field.clear()
    password_field.send_keys(password)

    # 4. Клик по кнопке отправки формы
    submit_button.click()
    return get_result_message(driver, STATUS_MESSAGE)


@pytest.mark.parametrize("email, password, expected_text", g_get_valid_params())
def test_positive_login(driver, email, password, expected_text):
    """Тест кейсы заполнения полей валидными данными"""

    actual_result = field_fills(driver=driver, email=email, password=password)
    assert expected_text in actual_result, f"Ожидался успешный вход, но получено: '{actual_result}'"


@pytest.mark.parametrize("email, password, expected_text", g_get_invalid_params())
def test_negative_login(driver, email, password, expected_text):
    """Тесты кейсы заполнения полей невалидными данными """

    actual_result = field_fills(driver=driver, email=email, password=password)
    assert expected_text in actual_result or driver.current_url != "success_url", \
        f"Форма пропустила некорректные данные: Email='{email}', Pass='{password}'"