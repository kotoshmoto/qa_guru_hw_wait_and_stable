from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

USERNAME_INPUT = (By.ID, "userName")
USER_EMAIL_INPUT = (By.ID, "userEmail")
CURRENT_ADDRESS_INPUT = (By.ID, "currentAddress")
PERMANENT_ADDRESS_INPUT = (By.ID, "permanentAddress")
SUBMIT_BUTTON = (By.ID, "submit")
OUTPUT_BLOCK = (By.ID, "output")


def test_field_fills(driver):
    # 1. Открытие тестовой страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")

    # 2. Заполнение полей формы
    driver.find_element(*USERNAME_INPUT).send_keys("Иван Иванов")
    driver.find_element(*USER_EMAIL_INPUT).send_keys("ivan@example.com")
    driver.find_element(*CURRENT_ADDRESS_INPUT).send_keys("ул. Ленина, дом 1")
    driver.find_element(*PERMANENT_ADDRESS_INPUT).send_keys("ул. Пушкина, дом 10")

    # Скролл до кнопки и клик
    submit_button = driver.find_element(*SUBMIT_BUTTON)
    driver.execute_script("arguments[0].scrollIntoView();", submit_button)
    submit_button.click()

    # 3. Настройка Fluent Wait
    # timeout: максимальное время ожидания (10 секунд)
    # poll_frequency: интервал опроса страницы (0.5 секунды)
    # ignored_exceptions: список игнорируемых исключений во время опроса
    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
    )

    # 4. Ожидание появления блока с результатами (id="output")
    output_block = fluent_wait.until(EC.visibility_of_element_located(OUTPUT_BLOCK))

    # 5. Проверка результата
    print("Тест успешно пройден! Блок с результатами появился.")
    assert output_block.is_displayed()
