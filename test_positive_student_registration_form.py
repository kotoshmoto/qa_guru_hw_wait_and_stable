from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import driver
from generators.student_registration_form_const import *
from helpers.close_banner_h import close_banner
from helpers.waiting_for_page_download_h import waiting_page_downloaded


def field_fills(driver, params):
    """Функция для заполнения полей """
    (firstname, lastname, user_email, gender_male, user_number, date_input,
     date_picker, month, year, subjects, curr_addr, state, city) = params

    url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
    wait = WebDriverWait(driver, 5)
    driver.get(url)

    # 0. Ожидаем загрузки страницы (проверяем видимость главного заголовка формы)
    waiting_page_downloaded(wait=wait)

    # 1. Убираем окно "Level up your automation" которое как минимум будет закрывать часть web element-ов
    # и мешать с ними работать!
    close_banner(wait=wait)

    # 2. Текстовые поля: Имя и Фамилия
    first_name = wait.until(EC.element_to_be_clickable(FIRSTNAME_INPUT))
    first_name.send_keys(firstname)

    last_name = driver.find_element(*LASTNAME_INPUT)
    last_name.send_keys(lastname)

    # 3. Текстовое поле: Email
    email = driver.find_element(*USER_EMAIL_INPUT)
    email.send_keys(user_email)

    # 4. Радиокнопки (Gender): кликаем по связанному тегу <label>, так как сам <input> скрыт
    gender_male_label = wait.until(EC.element_to_be_clickable(GENDER_MALE_LABEL))
    gender_male_label.find_element(*GENDER_MALE_LABEL)
    gender_male_label.click()

    # 5. Текстовое поле: Номер телефона (Mobile)
    mobile_number = driver.find_element(*USER_NUMBER_INPUT)
    mobile_number.send_keys(user_number)

    # 6. Виджет календаря (Date of Birth)
    date_input = driver.find_element(*DATE_INPUT)
    date_input.click()

    # Ожидаем появление всплывающего окна календаря
    wait.until(EC.visibility_of_element_located(DATE_PICKER))

    # Выбираем месяц (декабрь) через выпадающий список внутри календаря
    month_select = wait.until(EC.element_to_be_clickable(MONTH_SELECT))
    month_select.click()
    month_select.find_element(By.XPATH, "//option[@value='11']").click()  # 11 — это Декабрь

    # Выбираем год (1995)
    year_select = driver.find_element(*YEAR_SELECT)
    year_select.click()
    year_select.find_element(By.XPATH, "//option[@value='1995']").click()

    # Выбираем конкретный день месяца (например, 25-е число)
    # Используем специальный класс react-datepicker__day--025, исключая дни соседних месяцев (outside-month)
    day_element = driver.find_element(By.CSS_SELECTOR,
                                      ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
    day_element.click()

    # 7. Поле автодополнения (Subjects)
    subjects_input = wait.until(EC.element_to_be_clickable(SUBJECTS_INPUT))
    subjects_input.send_keys("Computer Science")
    subjects_input.send_keys(Keys.ENTER)

    # 8. Чекбоксы (Hobbies): кликаем по связанному <label>
    hobby_sports = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']"))
    )
    hobby_sports.click()

    hobby_music = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']")
    hobby_music.click()


def test_positive_field_fills_entire_form(driver):
    """Тест кейсы заполнения полей валидными данными """
