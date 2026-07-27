import pytest

from selenium import webdriver


@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Фоновый режим для CI/CD
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
