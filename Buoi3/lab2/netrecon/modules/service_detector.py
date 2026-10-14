import subprocess
import logging
import shutil
import os
from datetime import datetime

logging.basicConfig(filename='netrecon.log', level=logging.INFO)

def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[{now}] {msg}")

def get_nmap_cmd():
    if shutil.which("nmap"):
        return "nmap"
    default_path = r"C:\Program Files (x86)\Nmap\nmap.exe"
    if os.path.exists(default_path):
        return default_path
    return "nmap"

def detect_service(ip, ports):
    ports_str = ','.join(str(p) for p in ports)
    nmap_bin = get_nmap_cmd()
    cmd = [nmap_bin, "-sV", "-p", ports_str, ip]
    log(f"Running service detection on {ip}:{ports_str}")
    try:
        result = subprocess.check_output(cmd).decode()
        log(result)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode() if e.output else e}"
    except Exception as e:
        return f"Error: {e}"
