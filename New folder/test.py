import time
from selenium import webdriver as wd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


driver = wd.Chrome()
driver.get("https://vk.com/spearlex")
time.sleep(2)
element = driver.find_element(By.CLASS_NAME, "vkuiGroup__header")
element.click()
time.sleep(2)
for i in range(2):
    element = driver.find_element(By.ID, "layer_stl")
    ActionChains(driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
    time.sleep(1)


# driver.execute_script("arguments[0].scrollIntoView(true)", element)

# ActionChains(driver)\
#     .scroll_from_origin(scroll_origin, 0, 200)\
#     .perform()

time.sleep(2)
print(driver.page_source.encode("utf-8"))
driver.quit()

#
# def parsing():
#     URL = "https://vk.com/spearlex"
#     r = requests.get(URL)
#     soup = BeautifulSoup(r.content, features="xml")
#     print(r.text)
#
#
# parsing()