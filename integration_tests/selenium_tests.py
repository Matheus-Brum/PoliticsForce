import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def login_admin(self):
        driver = self.driver
        driver.get("http://localhost:5000")
        username = driver.find_element_by_id("champ_username")
        username.clear()
        username.send_keys("admin")
        password = driver.find_element_by_id("champ_password")
        password.clear()
        password.send_keys("admin123")
        password.send_keys(Keys.RETURN)

    def logout_admin(self):
        driver = self.driver
        driver.get("http://localhost:5000")
        wait = WebDriverWait(driver, 2)
        element = wait.until(EC.element_to_be_clickable((By.ID, 'logout_link')))
        link = driver.find_element_by_link_text('Se déconnecter')
        link.click()
        driver.close()

    def test_add_member(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        self.login_admin()
        # wait = WebDriverWait(driver, 10)
        # add = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'table')))
        link = driver.find_element_by_link_text('Ajouter un membre')
        link.click()
        first_name = driver.find_element_by_id("first_name")
        last_name = driver.find_element_by_id("last_name")
        member_no = driver.find_element_by_id("member_no")
        phone_no = driver.find_element_by_id("phone_no")
        country = Select(driver.find_element_by_id("country"))
        province = Select(driver.find_element_by_id("province"))
        city = Select(driver.find_element_by_id("city"))
        cp = driver.find_element_by_id("code-postal")
        appartement = driver.find_element_by_id("appartement")
        email = driver.find_element_by_id("email")
        last_donation = driver.find_element_by_id("last_donation")
        last_donation_date = driver.find_element_by_id("last_donation_date")
        is_donated = driver.find_element_by_id("donated_yes")
        is_elec = driver.find_element_by_id("elec_yes")
        expiring_date = driver.find_element_by_id("expiring_date")
        reach = driver.find_element_by_id("reach_day_morning")
        birth_date = driver.find_element_by_id("birth_date")
        committee = driver.find_element_by_id("committee")
        comment = driver.find_element_by_name("comment")
        first_name.clear()
        first_name.send_keys("John")
        last_name.clear()
        last_name.send_keys("Doe")
        member_no.clear()
        member_no.send_keys("0000000001")
        phone_no.clear()
        phone_no.send_keys("5141607890")
        country.select_by_value("US")
        wait.until(EC.element_to_be_clickable((By.ID, "AK")))
        province.select_by_value("AK")
        wait.until(EC.element_to_be_clickable((By.ID, "Anchorage")))
        city.select_by_value("Anchorage")
        cp.clear()
        cp.send_keys("A1A1A1")
        appartement.clear()
        appartement.send_keys("000")
        email.clear()
        email.send_keys("john-doe@gmail.com")
        last_donation.clear()
        last_donation.send_keys("25")
        last_donation_date.clear()
        last_donation_date.send_keys("01/01/2018")
        is_donated.click()
        is_elec.click()
        expiring_date.clear()
        expiring_date.send_keys("31/12/2018")
        reach.click()
        birth_date.clear()
        birth_date.send_keys("01/01/1990")
        committee.clear()
        committee.send_keys("Windy Association")
        comment.clear()
        comment.send_keys("This is a integration test")
        driver.find_element_by_id("submit_add").click()
        self.logout_admin()

    def test_modify_member(self):
        driver = self.driver
        wait = WebDriverWait(driver, 10)
        self.login_admin()
        driver.get("http://localhost:5000/afficher_membre/1234567890")
        time.sleep(5)
        link = driver.find_element_by_link_text('Modifier')
        link.click()
        time.sleep(5)
        # driver.find_element_by_id("reach_day_morning").click()
        # time.sleep(5)
        phone_no = driver.find_element_by_id("phone_no")
        phone_no.clear()
        phone_no.send_keys("2222222222")
        comment = driver.find_element_by_name("comment")
        comment.clear()
        comment.send_keys("this is an automated test!")
        time.sleep(5)
        driver.find_element_by_id("submit_modify").click()
        time.sleep(5)
        self.logout_admin()


if __name__ == "__main__":
    unittest.main()
