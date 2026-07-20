

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

APP_PASSWORD = "ggapfeaecwumiamg"

RECEIVER_EMAILS = [
    "vijayaravindan1208@gmail.com",
    "sonika.s@lk-ea.com"
]


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


people = pd.read_csv("people.csv")

initial_delay = random.randint(300, 2700)

print(f"\nInitial random delay: {initial_delay} seconds...\n")

time.sleep(initial_delay)

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    success_count = 0

    failed_people = []

    for _, person in people.iterrows():

        name = person["Name"]
        category = person["Category"]

        success = False

        # Retry once if first attempt fails
        for attempt in range(2):

            page = browser.new_page()

            try:

                current_time = datetime.now().strftime("%H:%M:%S")

                print(f"\n[{current_time}] Submitting for: {name} (Attempt {attempt + 1})")

                # Open Form
                page.goto(
                    FORM_URL,
                    wait_until="networkidle",
                    timeout=60000
                )

                # Click Start Now
                start_button = page.get_by_role(
                    "button",
                    name="Start now"
                )

                start_button.wait_for(
                    state="visible",
                    timeout=60000
                )

                start_button.click()

                # Name
                page.get_by_placeholder(
                    "Enter your answer"
                ).fill(name)

                # Category
                page.get_by_text(
                    category,
                    exact=False
                ).click()

                # Dining Area
                radios = page.locator("input[type='radio']")
                radios.last.click()

                # Submit
                page.get_by_role(
                    "button",
                    name="Submit"
                ).click()

                # Wait for submission to complete
                page.wait_for_timeout(5000)

                print(f"Submitted successfully: {name}")

                success_count += 1

                success = True

                page.close()

                break

            except Exception as e:

                print(f"Attempt {attempt + 1} failed for {name}")

                print(e)

                page.close()

                if attempt == 1:
                    failed_people.append(name)

                else:
                    print("Retrying...")

                    time.sleep(5)

        # Delay only after successful submission
        if success:

            delay = random.randint(20, 60)

            print(f"Waiting {delay} seconds...\n")

            time.sleep(delay)

    browser.close()

# =========================
# EMAIL NOTIFICATION
# =========================

if len(failed_people) == 0:

    send_email(
        "Machi Lunch Book Panten 😁👍",
        f"Nee sonna andha {success_count} people kum sethi panniten!"
    )

else:

    failed_text = "\n".join(failed_people)

    send_email(
        "Lunch Booking la prechana !!",
        f"Indha people-ku booking fail aagiruchu da:\n\n{failed_text}\n\nNee ivangaluku manual ah submit panniru."
    )

print("\nAll submissions completed.\n")
