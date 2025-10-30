import datetime

def log_crm_heartbeat():
    """
    DD/MM/YYYY-HH:MM:SS CRM is alive
    """

    datetime_now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("/tmp/crm_heartbeat.log", "a") as log_file:
        log_file.write(f"{datetime_now} CRM is alive\n")