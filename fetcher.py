# fetcher.py

import requests, io, base64
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# HICAS Portal URL
URL = "http://artsecampus.hicas.ac.in/hindusthan/"

def fetch_student_data(roll, password, dob):
    """
    Uses Selenium to login and fetch student info.
    Returns a dictionary with name, class, attendance, photo (base64).
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.set_page_load_timeout(30)
        driver.get(URL)

        # Fill the login form
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "data[MstUser][stud_user]"))
        )
        driver.find_element(By.NAME, "data[MstUser][stud_user]").send_keys(roll)
        driver.find_element(By.NAME, "data[MstUser][stud_password]").send_keys(password)
        driver.find_element(By.NAME, "data[MstUser][stud_dob]").send_keys(dob)
        driver.find_element(By.ID, "studentLoginButton").click()

        # Wait for the dashboard
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#student-info"))
        )

        # Extract data
        name = driver.find_element(By.CSS_SELECTOR, "#student-info > h1").text.strip()
        stu_class = driver.find_element(By.CSS_SELECTOR, "#student-info > h3 > span").text.strip()
        photo_url = driver.find_element(By.CSS_SELECTOR, "#photo > img").get_attribute("src")
        attendance = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "#content-container > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(1) > td:nth-child(3)"
            ))
        ).text.strip()

        # Convert photo to base64
        if photo_url:
            photo_response = requests.get(photo_url, timeout=5)
            photo_bytes = photo_response.content
            photo_base64 = "data:image/png;base64," + base64.b64encode(photo_bytes).decode()
        else:
            photo_base64 = None

        return {
            "status": "success",
            "name": name,
            "class": stu_class,
            "roll": roll,
            "attendance": attendance,
            "photo_base64": photo_base64
        }

    except Exception as e:
        return {
            "status": "fail",
            "message": str(e)
        }

    finally:
        if driver:
            driver.quit()
