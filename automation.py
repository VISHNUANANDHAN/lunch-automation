from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

FORM_URL = "https://forms.office.com/pages/responsepage.aspx?id=reFRbkvFOUu1mA_-muaP7_Bw656ZDoVIuISibW-uAYBUNkRINllQUEw2M09DUjI4STdMQ0FVTUs1Vy4u&route=shorturl"

# =========================
# EMAIL CONFIGURATION
# =========================

SENDER_EMAIL = "automationlunch@gmail.com"

APP_PASSWORD = "yrgggmmdebxwtbcc"

RECEIVER_EMAILS = [
    "vijayaravindan1208@gmail.com",
    "aravindan.v@lk-ea.com"
]

# =========================
# SEND EMAIL FUNCTION
# =========================

def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECEIVER_EMAILS)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAILS,
            msg.as_string()
        )

# =========================
# READ CSV DATA
# =========================

people = pd.read_csv("people.csv")

# =========================
# RANDOM INITIAL DELAY
# =========================

initial_delay = random.randint(300, 2700)

print(f"\nInitial random delay: {initial_delay} seconds...\n")

time.sleep(initial_delay)

# =========================
# PLAYWRIGHT AUTOMATION
# =========================

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    success_count = 0

    failed_people = []

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

            success_count += 1

            page.wait_for_timeout(3000)

            # RANDOM DELAY BETWEEN PEOPLE
            delay = random.randint(20, 60)

            print(f"Waiting {delay} seconds before next submission...\n")

            time.sleep(delay)

        except Exception as e:

            error_time = datetime.now().strftime("%H:%M:%S")

            print(f"[{error_time}] Error for {name}: {e}")

            failed_people.append(name)

    browser.close()

# =========================
# FINAL EMAIL NOTIFICATION
# =========================

if len(failed_people) == 0:

    send_email(
        "Lunch Automation Success",
        f"All {success_count} lunch forms submitted successfully."
    )

else:

    failed_text = "\n".join(failed_people)

    send_email(
        "Lunch Automation Partial Failure",
        f"Successful submissions: {success_count}\n\nFailed people:\n{failed_text}"
    )

print("\nAll submissions completed.\n")
