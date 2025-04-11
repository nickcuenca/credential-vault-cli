from datetime import datetime
import os

AUDIT_LOG_FILE = "vault_audit.log"

def log_action(action: str, site: str = None, status: str = "SUCCESS", note: str = ""):
    """
    Logs actions performed on the vault with timestamps.

    Args:
        action (str): Action performed (e.g., ADD, GET, DELETE)
        site (str): Site related to the action
        status (str): Status of the action (e.g., SUCCESS, FAILURE)
        note (str): Optional message for context
    """
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    site_part = f" | SITE: {site}" if site else ""
    note_part = f" ({note})" if note else ""
    line = f"{timestamp} ACTION: {action}{site_part} | STATUS: {status}{note_part}\n"

    try:
        with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as log:
            log.write(line)
    except Exception as e:
        print(f"⚠️ Failed to write to audit log: {e}")

def read_audit_log():
    if not os.path.exists(AUDIT_LOG_FILE):
        return "No audit log entries found."
    try:
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as log_file:
            return log_file.read()
    except Exception as e:
        return f"Failed to read audit log: {e}"