from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def close_banner(wait) -> None:
    # Ожидаем появление заголовка в модальном окне
    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))

    # Находим и кликаем по кнопке закрытия (крестику) модального окна
    close_banner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
    close_banner_btn.click()

    # Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
    wait.until(EC.invisibility_of_element(close_banner_btn))
