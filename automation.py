from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
from datetime import datetime

FORM_URL = "https://forms.office.com/pages/responsepage.aspx?id=reFRbkvFOUu1mA_-muaP7_Bw656ZDoVIuISibW-uAYBUNkRINllQUEw2M09DUjI4STdMQ0FVTUs1Vy4u&route=shorturl"

# READ PEOPLE DATA
people = pd.read_csv("people.csv")

# RANDOM INITIAL DELAY
# 5 minutes to 90 minutes
initial_delay = random.randint(5, 10)

print(f"\nInitial random delay: {initial_delay} seconds...\n")

time.sleep(initial_delay)

with sync_playwright() as p:

    # HEADLESS TRUE FOR CLOUD
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    for index, person in people.iterrows():

        try:

            name = person["Name"]
            category = person["Category"]

            current_time = datetime.now().strftime("%H:%M:%S")

            print(f"\n[{current_time}] Submitting for: {name}")

            # OPEN FORM
            page.goto(FORM_URL, timeout=60000)

            page.wait_for_timeout(3000)

            # CLICK START NOW
            page.get_by_role("button", name="Start now").click()

            page.wait_for_timeout(3000)

            # ENTER NAME
            page.get_by_placeholder("Enter your answer").fill(name)

            page.wait_for_timeout(1000)

            # SELECT CATEGORY
            page.get_by_text(category, exact=False).click()

            page.wait_for_timeout(2000)

            # SELECT DINING OPTION
            radios = page.locator("input[type='radio']")
            radios.last.click()

            page.wait_for_timeout(1000)

            # CLICK SUBMIT
            page.get_by_role("button", name="Submit").click()

            success_time = datetime.now().strftime("%H:%M:%S")

            print(f"[{success_time}] Submitted successfully: {name}")

            # WAIT AFTER SUBMIT
            page.wait_for_timeout(3000)

            # RANDOM DELAY BETWEEN PEOPLE
            delay = random.randint(3, 5)

            print(f"Waiting {delay} seconds before next submission...\n")

            time.sleep(delay)

        except Exception as e:

            error_time = datetime.now().strftime("%H:%M:%S")

            print(f"[{error_time}] Error for {name}: {e}")

    browser.close()

print("\nAll submissions completed.\n")
