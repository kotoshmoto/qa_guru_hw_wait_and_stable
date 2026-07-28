from generators.student_registration_form_const import *
from simple_test_student_registration_form import *


class TestAutomationForm:

    def test_fill_entire_form(self, driver):
        wait = WebDriverWait(driver, 5)  # Явное ожидание до 5 секунд
        url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

        driver.get(url)

        # 0. Ожидаем загрузки страницы (проверяем видимость главного заголовка формы)

        form_title = wait.until(EC.visibility_of_element_located(FORM_TITLE))
        assert form_title.text == "Practice Form"

        form_sub_title = wait.until(EC.visibility_of_element_located(FORM_SUB_TITLE))
        assert form_sub_title.text == "Student Registration Form"

        # 1. Убираем окно "Level up your automation" которое как минимум будет закрывать часть web element-ов
        # и мешать с ними работать!
        # Ожидаем появление заголовка в модальном окне
        wait.until(EC.visibility_of_element_located(POPUP_TITLE))
        # Находим и кликаем по кнопке закрытия (крестику) модального окна
        close_banner_btn = wait.until(EC.element_to_be_clickable(CLOSE_BANNER_BTN))
        close_banner_btn.click()

        # Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        wait.until(EC.invisibility_of_element(close_banner_btn))

        # 2. Текстовые поля: Имя и Фамилия
        first_name = wait.until(EC.element_to_be_clickable(FIRSTNAME_INPUT))
        first_name.send_keys("Иван")

        last_name = driver.find_element(*LASTNAME_INPUT)
        last_name.send_keys("Петров")

        # 3. Текстовое поле: Email
        email = driver.find_element(*USER_EMAIL_INPUT)
        email.send_keys("ivan.petrov@example.com")

        # 4. Радиокнопки (Gender): кликаем по связанному тегу <label>, так как сам <input> скрыт
        gender_male_label = wait.until(EC.element_to_be_clickable(GENDER_MALE_LABEL))
        gender_male_label.click()

        # 5. Текстовое поле: Номер телефона (Mobile)
        mobile_number = driver.find_element(*USER_NUMBER_INPUT)
        mobile_number.send_keys("9991234567")

        # 6. Виджет календаря (Date of Birth)
        date_input = driver.find_element(*DATE_INPUT)
        date_input.click()

        # Ожидаем появление всплывающего окна календаря
        wait.until(EC.visibility_of_element_located(DATE_PICKER))

        # Выбираем месяц (декабрь) через выпадающий список внутри календаря
        month_select = wait.until(EC.element_to_be_clickable(MONTH_SELECT))
        month_select.click()
        month_select.find_element(*MONTH_SELECT_DECEMBER).click()  # 11 — это Декабрь

        # Выбираем год (1995)
        year_select = driver.find_element(*YEAR_SELECT)
        year_select.click()
        year_select.find_element(*YEAR_SELECT_VALUE).click()

        # Выбираем конкретный день месяца (например, 25-е число)
        # Используем специальный класс react-datepicker__day--025, исключая дни соседних месяцев (outside-month)
        day_element = driver.find_element(*DAY_ELEMENT)
        day_element.click()

        # 7. Поле автодополнения (Subjects)
        subjects_input = wait.until(EC.element_to_be_clickable(SUBJECTS_INPUT))
        subjects_input.send_keys("Computer Science")
        subjects_input.send_keys(Keys.ENTER)

        # 8. Чекбоксы (Hobbies): кликаем по связанному <label>
        hobby_sports = wait.until(EC.element_to_be_clickable(HOBBY_SPORTS))
        hobby_sports.click()

        hobby_music = driver.find_element(*HOBBY_MUSIC)
        hobby_music.click()

        # 9. Загрузка файла (Picture)
        # Создаем временный файл для теста, чтобы код оставался переносимым
        temp_file_path = os.path.abspath("test_image.jpg")
        with open(temp_file_path, "w") as f:
            f.write("fake image data")

        upload_input = driver.find_element(*UPLOAD_INPUT)
        upload_input.send_keys(temp_file_path)

        # 10. Текстовая область: Текущий адрес (Current Address)
        current_address = driver.find_element(*CURRENT_ADDRESS_INPUT)
        current_address.send_keys("123456, г. Москва, ул. Ленина, д. 1")

        # Избавляемся от футеров или рекламы, которые могут перекрывать кастомные дропдауны, делаем скрол (главное, демонстрация execute_script)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")
        # driver.execute_script("document.getElementById('fixedban').style.display='none';")

        # 11. Выпадающий список (Dropdown): Выбор Штата (State)
        state_dropdown = wait.until(EC.element_to_be_clickable(STATE_DROPDOWN))
        state_dropdown.click()
        # Ждем появления опции во всплывающем меню дропдауна React-Select и кликаем
        state_option = wait.until(
            EC.element_to_be_clickable(STATE_OPTION))
        state_option.click()

        # 12. Выпадающий список (Dropdown): Выбор Города (City)
        city_dropdown = wait.until(EC.element_to_be_clickable(CITY_DROPDOWN))
        city_dropdown.click()
        city_option = wait.until(EC.element_to_be_clickable(CITY_OPTION))
        city_option.click()

        # 13. Отправка формы (Submit)
        submit_button = driver.find_element(*SUBMIT_BUTTON)
        driver.execute_script("arguments[0].click();", submit_button)  # Надежный клик через JS без перекрытий

        # 14. Проверка результатов (Expected Conditions для модального окна)
        # Проверяем, что появилось финальное окно с подтверждением
        modal_title = wait.until(EC.visibility_of_element_located(MODAL_TITLE))
        assert modal_title.text == "Thanks for submitting the form"

        # Проверяем наличие валидных данных в таблице результатов
        result_table = driver.find_element(By.CLASS_NAME, "table-responsive")
        assert "Иван Петров" in result_table.text
        assert "ivan.petrov@example.com" in result_table.text
        assert "Male" in result_table.text
        assert "9991234567" in result_table.text
        assert "25 Dec 1995" in result_table.text  # форма вывода даты может меняться от настроек
        assert "Computer Science" in result_table.text
        assert "Sports, Music" in result_table.text
        assert "test_image.jpg" in result_table.text
        assert "123456, г. Москва, ул. Ленина, д. 1" in result_table.text
        assert "NCR Delhi" in result_table.text

        # Удаляем созданный временный файл, если он существует
        if os.path.exists("test_image.jpg"):
            os.remove("test_image.jpg")
