from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests


def my_task(username, password, num):


    # gán option cho nó đỡ dính pool + optimal 
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    # vô trang mua acc
    driver.get("https://konichiwavps.com/Auth/Login")


    # log in
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="Login"]').click()

    check = True


    # func chờ tới khi web up acc
    while check:

        # check số lượng acc còn
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[3]/div[2]/div[1]/div[2]/div[3]/div/div/div/table/tbody/tr[1]/td[3]/b')))
        cnt = int(element.text)

        time.sleep(5)

        if cnt:
            # mua acc
            can_buy = num <= cnt if num else cnt
            driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[3]/div/div/div/table/tbody/tr[2]/td[6]/button').click()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="modal-soluong"]').clear()
            driver.find_element(By.XPATH, '//*[@id="modal-soluong"]').send_keys(can_buy)
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="btn-buy-now"]').click()

            # về lại dashbroad
            driver.get("https://konichiwavps.com/Dashbroad")

            print(f"Da mua {can_buy} acc")

            # end loop
            num -= can_buy
            if num == 0:
                check = False
        else:
            print("Chua len hang...")
            time.sleep(5)



def get_info(username, password):

    response = requests.get(f"https://konichiwavps.com/api/GetBalance.php?username={username}&password={password}")

    print(f"So du: {response.text}")
    
while True:
    username = input("Nhap username: ")
    password = input("Nhap password: ")
    get_info(username, password)

    num = int(input("Nhap so luong muon mua: "))
    my_task(username, password, num)
    print("done")
    