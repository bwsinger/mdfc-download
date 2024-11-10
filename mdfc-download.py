import os
import errno
import base64
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

input_file_path = "cards.txt"
output_path = "output"

# Create output directory
try:
    os.mkdir(output_path)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# driver = webdriver.Chrome(executable_path="chromedriver")
driver = webdriver.Chrome()

driver.get("https://dfcproxygenerator.web.app/")
driver.set_window_size(1296, 1440)
driver.implicitly_wait(3)
card_name_field = driver.find_element(By.ID, "cardName")

# Read from input file (./cards.txt) - each line should be the name of the front side of the mdfc

with open(input_file_path, "r+") as f_input:

    for line in f_input:
        # Clean line
        if len(line) > 3:
            card_name = line.strip('\n')
        else:
            continue

        card_name_field.clear()
        card_name_field.send_keys(card_name)

        time.sleep(0.5)

        try:
            name_option = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jss1 > .option"))
            )
        except:
            card_name_field.clear()
            continue

        name_option.click()

        # The homepage of the website loads a random card by default. Searching replaces
        # this card, but if you check for the one 'canvas' element immediately, it finds
        # the random one. Give the site just a second to remove the old canvas and then
        # explicitly wait for the new canvas to load.
        time.sleep(3)

        # Wait for proxy to load
        try:
            canvas = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "canvas"))
            )
        except:
            card_name_field.clear()
            continue

        # canvas = driver.find_element(By.TAG_NAME, "canvas")

        # save image (https://stackoverflow.com/questions/38316402/how-to-save-a-canvas-as-png-in-selenium/38318578#38318578#answer-38318578)

        # get the canvas as a PNG base64 string
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)

        # decode
        canvas_png = base64.b64decode(canvas_base64)

        file_name = f"{card_name} (Placeholder).png"

        # save the png
        with open(f"{output_path}/{file_name}", 'wb') as f:
            f.write(canvas_png)
