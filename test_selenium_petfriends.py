# Написать тест, который проверяет, что на странице со списком питомцев пользователя:
# Присутствуют все питомцы.
# Хотя бы у половины питомцев есть фото.
# У всех питомцев есть имя, возраст и порода.
# У всех питомцев разные имена.
# В списке нет повторяющихся питомцев. (Сложное задание).
# В первом тесте применяем явное ожидание. Во всех остальных неявное ожидание
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from settings import valid_email, valid_password
@pytest.fixture(autouse=True)
def testing():
    driver = webdriver.Chrome()

    # Задаем неявное ожидание
    driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    driver.get('http://petfriends.skillfactory.ru/login')

    yield driver
    driver.quit()


def test_my_pets_available():
    """ Проверяем что присутствуют все питомцы"""
    driver = webdriver.Chrome()
    driver.get('http://petfriends.skillfactory.ru/login')
    # Вводим email
    driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на ссылку мои питомцы
    driver.find_element_by_css_selector('a[href="/my_pets"]').click()
    # Явное ожидание при проверке таблицы питомцев.
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))
    # Поиск всех карточек питомцев
    list_my_pets = driver.find_elements_by_tag_name('tr')

    # Записываем в переменную статистику пользователя
    statistic_user = driver.find_element_by_xpath('//div[@class=".col-sm-4 left"]')
    # Сравниваем количество карточек с количеством питомцев в статистике. test1

    time.sleep(2)
    assert len(list_my_pets) - 1 == int(statistic_user.text.split()[2])

    # Проверяем, что мы оказались на странице пользователя
    assert driver.find_element_by_tag_name('h2').text == "alleksander67"

def test_my_pets_with_photo_half(testing):
    """ Проверяем что хотя бы у половины питомцев есть фото"""
    driver = testing  # транспортируем драйвер из фикстуры
    # Вводим email
    driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на ссылку мои питомцы
    driver.find_element_by_css_selector('a[href="/my_pets"]').click()

    # Явное ожидание при проверке таблицы питомцев.
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "all_my_pets")))

    # Поиск всех карточек питомцев
    list_my_pets = driver.find_elements_by_tag_name('tr')

    # Поиск всех карточек питомцев без фото
    pets_without_photo = driver.find_elements_by_css_selector("th > img[src='']")


    # Проверяем что хотя бы у половины питомцев есть фото
    # time.sleep(2)
    assert ((len(list_my_pets) - 1)/len(pets_without_photo)) >= 2

def test_my_pets_exists_name_age_breed(testing):
    """ Проверяем что у всех питомцев есть имя, возраст и порода"""
    driver = testing  # транспортируем драйвер из фикстуры
    # Вводим email
    driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на ссылку мои питомцы
    driver.find_element_by_css_selector('a[href="/my_pets"]').click()

    # Поиск всех имен, пород, возраста питомцев

    pet_name = driver.find_elements_by_xpath(('//td[1]'))
    pet_breed = driver.find_elements_by_xpath(('//td[2]'))
    pet_age = driver.find_elements_by_xpath(('//td[3]'))


    for i in range(len(pet_name)):
        assert pet_name[i].text != ''
        assert pet_breed[i].text != ''
        assert pet_age[i].text != ''
    # time.sleep(2)

def test_my_pets_different_names(testing):
    """ Проверяем что у всех питомцев разные имена"""
    driver = testing  # транспортируем драйвер из фикстуры
    # Вводим email
    driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на ссылку мои питомцы
    driver.find_element_by_css_selector('a[href="/my_pets"]').click()

    # Поиск всех имен
    pet_name = driver.find_elements_by_xpath(('//td[1]'))
    # Запускаем цикл где проверяем что имена питомцев не равны
    for i in range(len(pet_name)-1):
        for j in range(len(pet_name)):
            if j > i:
                assert pet_name[i].text != pet_name[j].text

    # time.sleep(2)

def test_my_pets_different_names(testing):
    """ Проверяем что в списке нет повторяющихся питомцев"""
    driver = testing  # транспортируем драйвер из фикстуры
    # Вводим email
    driver.find_element_by_id('email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element_by_id('pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на ссылку мои питомцы
    driver.find_element_by_css_selector('a[href="/my_pets"]').click()

    # Поиск всех имен, пород, возраста питомцев

    pet_name = driver.find_elements_by_xpath(('//td[1]'))
    pet_breed = driver.find_elements_by_xpath(('//td[2]'))
    pet_age = driver.find_elements_by_xpath(('//td[3]'))
    # Питомцы не повторяются если для всех питомцев поле имя или порода или возраст отличаются
    for i in range(len(pet_name)-1):
        for j in range(len(pet_name)):
            if j > i:
                assert (pet_name[i].text != pet_name[j].text) or (pet_breed[i].text != pet_breed[j].text) or \
                       (pet_age[i].text != pet_age[j].text)

    # time.sleep(2)