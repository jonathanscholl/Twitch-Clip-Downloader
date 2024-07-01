from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import datetime
import logging
import json
import time

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the folder containing videos to be uploaded
start_path = 'documents/private coding/twitch clips/final_clips'

def read_cookies(cookie_file):
    try:
        with open(cookie_file, 'r') as f:
            cookies = json.load(f)
        return cookies
    except FileNotFoundError:
        logging.error(f'Cookies file "{cookie_file}" not found.')
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON in cookies file: {e}')
    return None

def upload_video_to_tiktok(start_path, cookies_file):
    # Get list of video files in the specified directory
    list_folder = [f for f in os.listdir(start_path) if not f.startswith('.') and f.endswith('.mp4')]
    
    cookies = read_cookies(cookies_file)
    if cookies is None:
        logging.error('Failed to load cookies. Aborting upload.')
        return

    for index, clip in enumerate(list_folder):
        # Extract the streamer's name from the filename
        splitted_name = clip.rsplit('_', 1)
        if len(splitted_name) == 2:
            streamer_name = splitted_name[0]
        else:
            streamer_name = 'Unknown'

        # Get today's date and yesterday's date
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)

        # Format the date with periods instead of hyphens
        formatted_yesterday = yesterday.strftime("%d.%m.%Y")

        # Create the description for the video
        description = f' Top 3 Twitch Clips von {streamer_name} vom {formatted_yesterday} '
        
        hashtags = '#fyp #streamer #clips #streamerclips #twitch #deutschland'

        # Full path of the video
        video_path = os.path.join(start_path, clip)
        absolute_video_path = os.path.abspath(video_path)

        # Create a new WebDriver instance for each video upload
        options = webdriver.ChromeOptions()
  # Remove headless mode to visually debug if necessary
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # WebDriver is initialized inside the try block to ensure it is properly closed

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            
            # Navigate to the TikTok upload page
        driver.get("https://www.tiktok.com/upload")

            # Add cookies to the browser session
        for cookie in cookies:
                driver.add_cookie(cookie)

        driver.refresh()

        time.sleep(10)

            # Wait for the upload button to be clickable

        time.sleep(5)

        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
        file_input.send_keys(absolute_video_path)
        logging.info(f'Uploading video: {video_path}')

        time.sleep(15)      

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "DraftEditor-root")]//div[contains(@class, "public-DraftEditor-content")]')))
        description_input = driver.find_element(By.XPATH, '//div[contains(@class, "DraftEditor-root")]//div[contains(@class, "public-DraftEditor-content")]')

        description_input.click()
        description_input.clear()

        time.sleep(15)

        description_input.send_keys(description)
        logging.info(f'Entered description: {description}')


        time.sleep(10)

        description_input.send_keys(hashtags)

        time.sleep(20)

      
        schedule_button = driver.find_element(By.CLASS_NAME, 'jsx-3395700143 scheduled-picker')
        schedule_button.click()


        time.sleep(30)


        post_button = driver.find_element(By.CLASS_NAME, 'TUXButton')
        post_button.click() 

        time.sleep(10)


        """post_confirm_button = driver.find_element(By.CLASS_NAME, 'TUXButton TUXButton--default TUXButton--medium TUXButton--primary')
        post_confirm_button.click() """

        logging.info('Post button clicked. Waiting for video to be processed and posted.')

    

        time.sleep(50)





            

# Start uploading videos
cookies_file = 'documents/private coding/twitch clips/cookies.txt'
upload_video_to_tiktok(start_path, cookies_file)
