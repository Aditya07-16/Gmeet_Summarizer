import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

class MeetBot:
    def __init__(self, mail_address, password):
        self.mail_address = mail_address
        self.password = password
        self.driver = self.init_driver()

    def init_driver(self):
        opt = Options()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })
        return webdriver.Chrome(options=opt)

    def login(self):
        self.driver.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')
        wait = WebDriverWait(self.driver, 20)

        # Input Gmail
        wait.until(EC.element_to_be_clickable((By.ID, "identifierId"))).send_keys(self.mail_address)
        wait.until(EC.element_to_be_clickable((By.ID, "identifierNext"))).click()

        # Wait for the password field to be interactive
        password_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="password"]')))
        password_field.send_keys(self.password)
        wait.until(EC.element_to_be_clickable((By.ID, "passwordNext"))).click()

        # Go to Google home page
        self.driver.get('https://google.com/')
        time.sleep(3)  # Wait for the page to load completely

    def turnOffMicCam(self):
        wait = WebDriverWait(self.driver, 30)

        try:
            mic_button_xpath = "//div[contains(@aria-label, 'microphone')]"
            mic = wait.until(EC.element_to_be_clickable((By.XPATH, mic_button_xpath)))
            mic.click()
            print("Microphone toggled.")
        except TimeoutException:
            print("Failed to find or click the microphone button.")

        try:
            cam_button_xpath = "//div[contains(@aria-label, 'camera')]"
            camera = wait.until(EC.element_to_be_clickable((By.XPATH, cam_button_xpath)))
            camera.click()
            print("Camera toggled.")
        except TimeoutException:
            print("Failed to find or click the camera button.")

    def joinNow(self):
        wait = WebDriverWait(self.driver, 20)
        try:
            join_xp = "//*[@id=\"yDmH0d\"]/c-wiz/div/div/div[27]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button"
            join = wait.until(EC.element_to_be_clickable((By.XPATH, join_xp)))
            join.click()
            time.sleep(10)
        except TimeoutException:
            print("Failed to find the join button. Check the element's visibility or selector.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

# Usage
mail_address = 'adibhat0716@gmail.com'
password = 'p@s$word123'
bot = MeetBot(mail_address, password)
bot.login()
bot.driver.get('https://meet.google.com/txu-hnkp-zmt')
bot.turnOffMicCam()
bot.joinNow()
