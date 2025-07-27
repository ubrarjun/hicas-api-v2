# fetcher.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import csv
import time

def fetch_student_data(roll, password, dob):
    try:
        # Setup headless Chrome
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(20)

        # Step 1: Open login page
        driver.get("http://artsecampus.hicas.ac.in/hindusthan/")  # ✅ Corrected


        # Step 2: Input credentials
        driver.find_element(By.ID, "txtregno").send_keys(roll)
        driver.find_element(By.ID, "txtpassword").send_keys(password)
        driver.find_element(By.ID, "txtdob").send_keys(dob)
        driver.find_element(By.ID, "btnSubmit").click()

        time.sleep(2)

        # Step 3: Scrape student info
        name = driver.find_element(By.ID, "lblname").text
        student_class = driver.find_element(By.ID, "lblclass").text
        attendance = driver.find_element(By.ID, "lblattenpercent").text
        photo = driver.find_element(By.ID, "imgPhoto").get_attribute("src")

        driver.quit()

        # Step 4: Save admin log
        log_user_info(roll, dob, name, photo)

        return {
            "status": "success",
            "name": name,
            "class": student_class,
            "attendance": attendance,
            "photo": photo
        }

    except TimeoutException:
        return {"status": "fail", "message": "Timeout error while loading the page."}
    except WebDriverException as e:
        return {"status": "fail", "message": f"WebDriver error: {str(e)}"}
    except Exception as e:
        return {"status": "fail", "message": f"Unexpected error: {str(e)}"}

def log_user_info(roll, dob, name, photo_url):
    try:
        with open("users_log.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), roll, dob, name, photo_url])
    except Exception as e:
        print("Logging error:", e)
