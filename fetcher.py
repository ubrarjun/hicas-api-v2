from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
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

        # Step 1: Open correct login page
        driver.get("http://artsecampus.hicas.ac.in/hindusthan/")

        # Step 2: Input credentials using correct name attributes
        driver.find_element(By.NAME, "data[MstUser][stud_user]").send_keys(roll)
        driver.find_element(By.NAME, "data[MstUser][stud_password]").send_keys(password)
        driver.find_element(By.NAME, "data[MstUser][stud_dob]").send_keys(dob)

        # Step 3: Click login button by ID
        driver.find_element(By.ID, "studentLoginButton").click()
        time.sleep(2)

        # Step 4: Scrape student info (Update these IDs once you confirm after login)
        name = driver.find_element(By.ID, "student_name").text
        student_class = driver.find_element(By.ID, "student_class").text
        attendance = driver.find_element(By.ID, "student_attendance").text
        photo = driver.find_element(By.ID, "student_photo").get_attribute("src")

        driver.quit()

        # Save admin log
        log_user_info(roll, dob, name, photo)

        return {
            "status": "success",
            "name": name,
            "class": student_class,
            "attendance": attendance,
            "photo": photo
        }

    except NoSuchElementException:
        return {"status": "fail", "message": "Some element not found. Confirm correct field IDs after login."}
    except TimeoutException:
        return {"status": "fail", "message": "Timeout error while loading the page."}
    except WebDriverException as e:
        return {"status": "fail", "message": f"WebDriver error: {str(e)}"}
    except Exception as e:
        return {"status": "fail", "message": f"Unexpected error: {str(e)}"}
    finally:
        try:
            driver.quit()
        except:
            pass

def log_user_info(roll, dob, name, photo_url):
    try:
        with open("users_log.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), roll, dob, name, photo_url])
    except Exception as e:
        print("Logging error:", e)
