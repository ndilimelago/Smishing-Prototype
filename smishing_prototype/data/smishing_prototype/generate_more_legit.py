"""
generate_more_legit.py
------------------------
Adds a further batch of DIVERSE legitimate SMS examples to rebalance
the dataset (223 suspicious vs 109 legitimate before this run).

Uses different templates/structures to the original batch so the
classifier learns genuine legitimate-message characteristics rather
than a narrow set of sentence shapes.
"""

import csv
import random
import pandas as pd

random.seed(7)

names = ["Julia", "Markus", "Beatha", "Ndeshi", "Tangeni", "Simeon", "Ester",
         "Petrus", "Ndapewa", "Johannes", "Helvi", "Absalom", "Ainna", "Frieda",
         "Rauna", "Immanuel", "Selma", "Paulus", "Meme", "Erastus"]
banks = ["FNB", "Bank Windhoek", "Nedbank Namibia", "Standard Bank Namibia"]
telcos = ["MTC", "TN Mobile"]
amounts = [20, 35, 50, 75, 100, 120, 150, 200, 250, 300, 400, 500, 600, 750, 900, 1200]
merchants = ["Woermann Brock", "Pick n Pay", "Model Pharmacy", "Shoprite", "Metro",
             "Checkers", "Spar Windhoek", "Ark Trading", "Model Supermarket"]
places = ["Windhoek", "Oshakati", "Swakopmund", "Walvis Bay", "Rundu", "Ongwediva",
          "Otjiwarongo", "Katima Mulilo"]

rows = []

def add(msg):
    rows.append(("legitimate", msg))

# --- Group 1: Everyday personal texts (no transaction at all) ---
personal_templates = [
    "Hey {name}, are you free to chat later tonight?",
    "{name}, don't forget we have a group assignment meeting tomorrow at 2pm.",
    "Good morning! Hope you slept well. See you at campus.",
    "Can you send me the notes from today's lecture when you get a chance?",
    "{name}, happy birthday! Hope you have an amazing day.",
    "Running a bit late, be there in 10 minutes.",
    "Thanks for helping me move the furniture yesterday, really appreciated it.",
    "Let's meet at the usual spot after class, same time as last week.",
    "Congrats on passing your exams {name}! So proud of you.",
    "Can we reschedule our call to Friday instead of Thursday?",
    "Don't forget to bring your ID card for registration tomorrow.",
    "The braai is still on for Saturday, bring your own drinks.",
    "{name}, is the WiFi working at res today? Mine keeps dropping.",
    "Miss you loads, call me when you're free this weekend.",
]
for t in personal_templates:
    for _ in range(3):
        add(t.format(name=random.choice(names)))

# --- Group 2: Utility / service reminders ---
service_templates = [
    "Reminder: Your water account is due on the 25th of this month. Pay via the municipal office or online portal.",
    "Your prepaid electricity balance is running low. Top up soon to avoid disconnection.",
    "NamWater: Your account statement for this month is now available at your nearest office.",
    "City of {place}: Refuse collection will take place on Thursday this week instead of Wednesday.",
    "Reminder: Your library books are due for return by Friday. Renew online to avoid a fine.",
    "UNAM: Semester fees are due by the end of this month. Visit the finance office for details.",
    "NBC: Don't miss tonight's 8 o'clock news bulletin.",
    "Namib Mills: Thank you for choosing our products. Follow us for recipes and specials.",
    "Reminder: Your gym membership renews in 3 days. Visit reception to update your payment details.",
    "Your municipal rates statement is ready for collection at the {place} municipal office.",
]
for t in service_templates:
    for _ in range(3):
        add(t.format(place=random.choice(places)))

# --- Group 3: Bank/eWallet notifications with varied structure ---
bank_templates = [
    "{bank}: Your balance enquiry shows N${amt} available in your account as at today.",
    "{bank}: A recurring debit order of N${amt} for insurance was processed today.",
    "{bank}: Your card ending {digits} was used for a purchase of N${amt} at {merchant}.",
    "{bank} Notice: Your cheque deposit of N${amt} has been credited to your account.",
    "{bank}: Your loan instalment of N${amt} was successfully deducted today. Thank you.",
    "{bank}: Your fixed deposit of N${amt} matures on the 30th of this month.",
    "{bank}: Your account was credited with N${amt} as monthly interest.",
    "{bank}: Your recent ATM withdrawal of N${amt} was successful. Balance: N${bal}.",
    "eWallet: Your voucher of N${amt} has been redeemed successfully.",
    "eWallet: You have successfully paid your DStv subscription of N${amt}.",
    "{bank}: Please note our branch will close early on Friday for staff training.",
    "{bank}: Your new debit card is ready for collection at your nearest branch.",
]
for t in bank_templates:
    for _ in range(3):
        add(t.format(
            bank=random.choice(banks), amt=random.choice(amounts),
            bal=random.choice(amounts) * 2, digits=random.randint(1000, 9999),
            merchant=random.choice(merchants),
        ))

# --- Group 4: Telecom notifications with varied structure ---
telco_templates = [
    "{telco}: You have used 80% of your monthly data bundle. Consider topping up soon.",
    "{telco}: Your subscription to the ringtone service has been renewed for N${amt}.",
    "{telco}: Thank you for topping up N${amt}. Your new airtime balance is N${bal}.",
    "{telco}: Free 50MB night data has been added to your account, valid until 5am.",
    "{telco}: Your bill for this month is N${amt}, due on the 7th. Pay via the {telco} app.",
    "{telco}: Welcome to our postpaid family! Your first invoice will arrive next month.",
    "{telco}: Network maintenance is scheduled in your area tonight from 11pm to 2am.",
    "{telco}: Your number has been successfully ported. Welcome aboard!",
]
for t in telco_templates:
    for _ in range(3):
        telco = random.choice(telcos)
        add(t.format(telco=telco, amt=random.choice(amounts), bal=random.choice(amounts)*3))

# --- Group 5: Appointment / institutional reminders ---
institutional_templates = [
    "Reminder: Your dental appointment at {place} Dental Clinic is on Tuesday at 09:00.",
    "MVA Fund: Your vehicle licence renewal is due this month. Visit NaTIS for assistance.",
    "Namibian Police: Community meeting on neighbourhood safety this Saturday at the hall, 10am.",
    "Ministry of Health: Free health screening at {place} clinic this week, all welcome.",
    "Your parcel from {merchant} is ready for collection at the {place} branch.",
    "NamPost: Your registered letter has arrived and is ready for collection.",
    "Reminder: School fees for the term are due by the 15th. Contact the bursar for a statement.",
    "Your vehicle service at {place} Motors is booked for Wednesday at 08:30.",
]
for t in institutional_templates:
    for _ in range(3):
        add(t.format(place=random.choice(places), merchant=random.choice(merchants)))

# --- Deduplicate against nothing yet (final merge script handles cross-file dedup) ---
seen = set()
unique_rows = []
for label, msg in rows:
    if msg not in seen:
        seen.add(msg)
        unique_rows.append((label, msg))

print(f"Generated {len(unique_rows)} new legitimate messages")

with open("data/new_legit_batch.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["label", "message"])
    writer.writerows(unique_rows)
