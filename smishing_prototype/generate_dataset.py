"""
generate_dataset.py
--------------------
Builds an expanded data/sms_dataset.csv of SIMULATED SMS messages.

Every 'suspicious' message below is modelled on a real, documented
Namibian eWallet/mobile-money fraud pattern (see the SOURCE comment
on each template group) -- NOT copied verbatim from any real message,
since actual scam wording is not published by banks/telecoms/news for
security reasons. This mirrors the approach described in the thesis
(Section 3.5): simulated examples developed from documented fraud
patterns, used because real scam-message corpora are not accessible.

SOURCES used to model the patterns:
- The Namibian (2023) "Thieves targeting FNB customers through eWallet"
- FNB / Namibian Sun (2022) "FNB warns against eWallet scam" (OTP-linking pattern)
- Bank Windhoek / Bankers Association of Namibia scam warning (fake prize/winnings pattern)
- Telecom Namibia Fraud Report (SMS reward-for-information pattern)
"""

import csv
import random

random.seed(42)

names = ["Julia", "Markus", "Beatha", "Ndeshi", "Tangeni", "Simeon", "Ester",
         "Petrus", "Ndapewa", "Johannes", "Helvi", "Absalom", "Ainna", "Frieda"]
banks = ["FNB", "Bank Windhoek", "Nedbank Namibia", "Standard Bank Namibia"]
telcos = ["MTC", "TN Mobile"]
amounts = [50, 80, 100, 150, 200, 250, 300, 450, 500, 800, 1000, 1500]
links = ["bit.ly/verify-ew", "secure-ewallet.tk", "namclaim.link",
         "confirm-acc.cf", "bankwin-secure.tk", "mtc-reward.ga"]

rows = []

def add(label, msg):
    rows.append((label, msg))

# ---------------------------------------------------------------
# SUSPICIOUS: Pattern 1 -- OTP-linking scam (FNB, 2022)
# Real mechanism: fraudster triggers a genuine OTP prompt by trying to
# link the victim's number to their own device, then a message/call
# pressures the victim to read out or forward that OTP.
# ---------------------------------------------------------------
otp_link_templates = [
    "{bank}: A request was made to link your eWallet to a new device. Reply with the OTP sent to you to confirm this was you.",
    "{bank} eWallet: Someone attempted to register your number on a new phone. Send the 4-digit OTP now to cancel this request.",
    "Your {bank} eWallet is being set up on a new device. If you did not request this, reply with your OTP immediately to stop it.",
    "{bank} Alert: OTP requested for eWallet verification. Forward the code you just received to complete the security check.",
    "eWallet Security: A new device tried to access your wallet. Confirm it wasn't you by texting back the OTP code.",
    "{bank}: Your OTP is required to reverse an unauthorised wallet-linking attempt. Reply with the code within 5 minutes.",
]
for t in otp_link_templates:
    for bank in banks:
        add("suspicious", t.format(bank=bank))

# ---------------------------------------------------------------
# SUSPICIOUS: Pattern 2 -- Fake prize / winnings scam (Bank Windhoek warning)
# Real mechanism: SMS claims the recipient has won a prize, then a call
# guides them to "withdraw" or transfer funds to release the winnings.
# ---------------------------------------------------------------
prize_templates = [
    "Congratulations {name}! Your number has been selected to win N${amt}0 in the {telco} promo. Call this number to claim your prize.",
    "You have won N${amt}0 from the {bank} customer rewards draw! Reply with your eWallet number to receive your winnings today.",
    "GOOD NEWS: You are a lucky winner of N${amt}0! Send your ID and PIN to our agent to process your prize withdrawal.",
    "{telco} Promo: Your SIM has won a cash prize of N${amt}0. Visit {link} and enter your PIN to claim before it expires.",
    "Dear winner, your entry has been selected for a N${amt}0 payout. Kindly provide your account details to release the funds.",
]
for t in prize_templates:
    for _ in range(5):
        name = random.choice(names)
        bank = random.choice(banks)
        telco = random.choice(telcos)
        amt = random.choice(amounts)
        link = random.choice(links)
        add("suspicious", t.format(name=name, bank=bank, telco=telco, amt=amt, link=link))

# ---------------------------------------------------------------
# SUSPICIOUS: Pattern 3 -- Reward-for-information scam (Telecom Namibia)
# Real mechanism: SMS from a local mobile number offers a reward in
# exchange for personal information.
# ---------------------------------------------------------------
reward_info_templates = [
    "Hi, this is {telco} customer care. Confirm your ID number and date of birth to receive your loyalty reward of N${amt}.",
    "{telco} Rewards: Complete this quick survey and share your account PIN to receive a free N${amt} airtime voucher.",
    "You qualify for a free {telco} data bundle. Reply with your name, ID number and PIN to activate it today.",
    "Free gift alert: {telco} is giving away N${amt} to selected customers. Send your personal details to claim yours now.",
]
for t in reward_info_templates:
    for telco in telcos:
        for amt in random.sample(amounts, 3):
            add("suspicious", t.format(telco=telco, amt=amt))

# ---------------------------------------------------------------
# SUSPICIOUS: Pattern 4 -- Account suspension / urgency threat
# ---------------------------------------------------------------
urgency_templates = [
    "{bank}: Your account will be suspended within 24 hours due to unusual activity. Verify your PIN now to prevent this.",
    "URGENT {bank} NOTICE: Your eWallet access will be blocked today unless you confirm your OTP immediately.",
    "Final warning from {bank}: Your card has been flagged. Call now and provide your PIN or it will be permanently locked.",
    "{bank} Security: Unauthorised login detected. Your account will be closed in 1 hour unless you verify your details.",
    "Your eWallet will expire today. Send your PIN now to keep your account active and avoid losing your funds.",
]
for t in urgency_templates:
    for bank in banks:
        add("suspicious", t.format(bank=bank))

# ---------------------------------------------------------------
# SUSPICIOUS: Pattern 5 -- Refund / fee request + suspicious link
# ---------------------------------------------------------------
refund_fee_templates = [
    "{bank} Refund Notice: You are owed N${amt} from a failed transaction. Click {link} and enter your PIN to receive it.",
    "Your parcel is held at customs. Pay a clearance fee of N${amt} via {link} to release your delivery today.",
    "{bank}: A reversal of N${amt} is pending on your account. Confirm your card PIN at {link} to receive the funds.",
    "Refund available: N${amt} will be credited once you verify your account at {link}. Do this within 24 hours.",
]
for t in refund_fee_templates:
    for bank in banks:
        for amt in random.sample(amounts, 2):
            link = random.choice(links)
            add("suspicious", t.format(bank=bank, amt=amt, link=link))

# ---------------------------------------------------------------
# LEGITIMATE: real-style transaction/service notifications
# ---------------------------------------------------------------
legit_templates_person = [
    "Your eWallet transaction of N${amt} to {name} was successful. Available balance: N${bal}.",
    "You have received N${amt} from {name} via eWallet. New balance: N${bal}.",
    "{bank}: A debit of N${amt} was made on your account ending {digits}. Available balance N${bal}.",
    "{bank}: You have received N${amt} from {name}. Reference: {ref}.",
    "Your {telco} airtime purchase of N${amt} was successful. Enjoy!",
    "Your {telco} data bundle purchase of {amt}MB was successful and is valid for 30 days.",
    "Reminder: Your {telco} prepaid balance is low. Top up via the {telco} app or nearest agent.",
    "Your salary of N${sal} has been deposited into your account ending {digits}.",
    "{bank}: Your monthly statement is now available. Log in to the official {bank} app to view it.",
    "Thank you for your payment of N${amt} to {merchant}. Reference: {ref}.",
    "Your {bank} OTP is {otp}. Do not share this code with anyone. Valid for 5 minutes.",
    "Reminder from UNAM: Registration for the semester closes soon. Visit the student portal for details.",
    "Hi {name}, are we still meeting at the library at {time}? Let me know.",
    "Your electricity token is {token} for N${amt}. Thank you for using NamPower.",
    "Appointment reminder: Your appointment with Dr {name} is scheduled for tomorrow at {time}.",
]
merchants = ["Woermann Brock", "Pick n Pay", "Model Pharmacy", "Shoprite", "Metro"]

for t in legit_templates_person:
    for _ in range(9):
        name = random.choice(names)
        bank = random.choice(banks)
        telco = random.choice(telcos)
        amt = random.choice(amounts)
        bal = random.choice(amounts) * 3
        sal = random.choice([4500, 6200, 7800, 8500, 9200])
        digits = random.randint(1000, 9999)
        ref = f"{random.choice(['EW','FNB','BW'])}{random.randint(10000,99999)}"
        otp = random.randint(100000, 999999)
        time_ = random.choice(["10:00", "14:30", "3pm", "9:00", "16:00"])
        token = "-".join(str(random.randint(1000,9999)) for _ in range(5))
        merchant = random.choice(merchants)
        try:
            msg = t.format(name=name, bank=bank, telco=telco, amt=amt, bal=bal,
                            sal=sal, digits=digits, ref=ref, otp=otp, time=time_,
                            token=token, merchant=merchant)
            add("legitimate", msg)
        except KeyError:
            pass

# ---------------------------------------------------------------
# Deduplicate + write CSV
# ---------------------------------------------------------------
seen = set()
unique_rows = []
for label, msg in rows:
    if msg not in seen:
        seen.add(msg)
        unique_rows.append((label, msg))

random.shuffle(unique_rows)

with open("data/sms_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["label", "message"])
    writer.writerows(unique_rows)

n_susp = sum(1 for l, _ in unique_rows if l == "suspicious")
n_legit = sum(1 for l, _ in unique_rows if l == "legitimate")
print(f"Wrote {len(unique_rows)} messages -> data/sms_dataset.csv")
print(f"  suspicious: {n_susp}")
print(f"  legitimate: {n_legit}")
