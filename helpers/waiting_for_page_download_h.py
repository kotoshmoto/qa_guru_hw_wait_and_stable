from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def waiting_page_downloaded(wait) -> None:
    form_title = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/h1")))
    assert form_title.text == "Practice Form"

    form_sub_title = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/div/p")))
    assert form_sub_title.text == "Student Registration Form"
