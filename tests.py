import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    _driver = webdriver.Chrome('./chromedriver.exe')

    yield _driver

    _driver.quit()


@pytest.fixture
def authorized_driver(driver):
    driver.get('http://petfriends.skillfactory.ru/login')
    driver.find_element(By.ID, 'email').send_keys("test13@test.ru")
    driver.find_element(By.ID, 'pass').send_keys('123')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    return driver


def test_show_my_pets(authorized_driver):
    driver = authorized_driver
    driver.get('http://petfriends.skillfactory.ru/my_pets')
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-img-top')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck.card-img-top')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != '', "Image not found"
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        kind, age = descriptions[i].text.split(", ")
        assert len(kind) > 0
        assert len(age) > 0


@pytest.fixture
def my_pets(authorized_driver):
    authorized_driver.implicitly_wait(2)
    authorized_driver.get('http://petfriends.skillfactory.ru/my_pets')
    div_all_my_pets = authorized_driver.find_element(By.ID, "all_my_pets")
    assert div_all_my_pets is not None

    title_founded = WebDriverWait(authorized_driver, 5).until(
        EC.title_contains('PetFriends: My Pets')
    )
    assert title_founded

    return authorized_driver

#Присутствуют все питомцы
def test_check_my_pet(my_pets):
    pet_tag = authorized_driver.find_element(By.XPATH, "//div[contains(@class,'task3')]/div[1]")
    pet_count = int(pet_tag.text.split('\n')[1].split(':')[1])
    pet_rows = authorized_driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr")
    assert pet_count == len(pet_rows)


# Хотя бы у половины питомцев есть фото.
def test_check_half_pets_have_photo(my_pets):
    pet_images = my_pets.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/th/img")
    counter = 0
    for i in range(len(pet_images)):
        if pet_images[i].get_attribute('src') != 'unknown':
            counter += 1
    assert counter >= len(pet_images) / 2


# У питомцев есть имя, возраст и порода.
def test_pet_has_name_kind_age(my_pets):
    pet_data_complect = my_pets.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td")

    for pet_data in pet_data_complect:
        assert pet_data.text.strip() != ""


# У питомцев разные имена.
def test_all_names_are_different(my_pets):
    td_names = my_pets.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td[1]")
    pet_names = []
    for td_name in td_names:
        pet_names.append(td_name.text)
    assert len(pet_names) == len(set(pet_names))


# В списке нет повторяющихся питомцев. (Сложное задание).
def test_all_pets_are_different(my_pets):
    tr_pets = my_pets.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr")
    pets = []

    for tr_pet in tr_pets:
        pets.append(tr_pet.text)

    assert len(set(pets)) == len(pets)
