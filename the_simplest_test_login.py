import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
SUBMIT_BUTTON = (By.ID, "submit-button")
STATUS_MESSAGE = (By.ID, "error-message")


@pytest.fixture()
def driver():
    # 1. Инициализация браузера
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_field_fills(driver):
    # 2. Открытие страницы авторизации
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    driver.maximize_window()

    wait = WebDriverWait(driver, 20)

    # 3. Поиск элементов и заполнение формы
    driver.find_element(*LOGIN_INPUT).send_keys("qaguru@gmail.com")
    driver.find_element(*PASSWORD_INPUT).send_keys("qagurupassword")

    # 4. Нажатие кнопки "Войти"
    submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON))
    submit_button.click()

    # 5. Проверка того что входные данные не подходят (проверяем наличие элемента на новой странице)
    error_message = driver.find_element(*STATUS_MESSAGE).text
    time.sleep(5)

    assert "Wrong login or password" in error_message
    print("Тест пройден успешно! Вввели неверные данные и не смогли войти в систему.")
