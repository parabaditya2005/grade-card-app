import pandas as pd
import os

def log_email_status(name, email, status, log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "email_log.csv")

    entry = pd.DataFrame([[name, email, status]], columns=["Name", "Email", "Status"])

    if os.path.exists(log_file):
        old = pd.read_csv(log_file)
        new = pd.concat([old, entry], ignore_index=True)
        new.to_csv(log_file, index=False)
    else:
        entry.to_csv(log_file, index=False)
