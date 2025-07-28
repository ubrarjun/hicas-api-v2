import requests
import base64
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# HICAS student portal URL
URL = "http://artsecampus.hicas.ac.in/hindusthan/"

def fetch_student_data(roll, password, dob):
    options = Options()
    options.add_argument("--headless")  # headless mode for server
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_preference("dom.webnotifications.enabled", False)

    service = Service("/usr/local/bin/geckodriver")  # Render path

    driver = None
    try:
        driver = webdriver.Firefox(options=options, service=service)
        driver.set_page_load_timeout(30)
        driver.get(URL)

        # Wait and fill login form
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "data[MstUser][stud_user]"))
        )
        driver.find_element(By.NAME, "data[MstUser][stud_user]").send_keys(roll)
        driver.find_element(By.NAME, "data[MstUser][stud_password]").send_keys(password)
        driver.find_element(By.NAME, "data[MstUser][stud_dob]").send_keys(dob)
        driver.find_element(By.ID, "studentLoginButton").click()

        # Wait for student dashboard
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "student-info"))
        )

        # Extract info
        name = driver.find_element(By.CSS_SELECTOR, "#student-info > h1").text.strip()
        stu_class = driver.find_element(By.CSS_SELECTOR, "#student-info > h3 > span").text.strip()
        photo_url = driver.find_element(By.CSS_SELECTOR, "#photo > img").get_attribute("src")
        attendance = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "#content-container > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td:nth-child(3)"))
        ).text.strip()

        # Convert photo to base64
        photo_base64 = None
        if photo_url:
            photo_bytes = requests.get(photo_url, timeout=5).content
            photo_base64 = "data:image/png;base64," + base64.b64encode(photo_bytes).decode()

        return {
            "status": "success",
            "name": name,
            "class": stu_class,
            "roll": roll,
            "attendance": attendance,
            "photo_base64": photo_base64
        }

    except Exception as e:
        return {"status": "fail", "message": str(e)}
    finally:
        if driver:
            driver.quit()
