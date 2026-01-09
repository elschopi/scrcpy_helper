import subprocess
import time
import re
import os
import sys

ip = "192.168.178.107"

# --- KONFIGURATION ---
nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"

if not os.path.exists(nmap_path):
    nmap_path = r"C:\Program Files\Nmap\nmap.exe"

if not os.path.exists(nmap_path):
    print(f"WARNUNG: nmap.exe wurde nicht unter {nmap_path} gefunden.")
    nmap_cmd = "nmap" 
else:
    nmap_cmd = f'"{nmap_path}"'

# --- PFAD LOGIK FÜR EXE ---
# Das ist der entscheidende Teil für die EXE
if getattr(sys, 'frozen', False):
    # Wenn wir als EXE laufen, nimm den Ordner, in dem die .exe liegt
    script_dir = os.path.dirname(sys.executable)
    print(f"DEBUG: Starte als EXE aus: {script_dir}")
else:
    # Wenn wir als Skript laufen, nimm den Ordner der .py Datei
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"DEBUG: Starte als Python-Skript aus: {script_dir}")

scrcpy_path = os.path.join(script_dir, "scrcpy.exe")

print(f"Suche scrcpy unter: {scrcpy_path}")
print(f"Nutze Nmap unter: {nmap_path}")
print(f"Scanne {ip} auf Ports 30000-51000 (bitte warten)...")

# 1. Nmap ausführen
command = f"& {nmap_cmd} {ip} -p 30000-51000"

ret = subprocess.run(["powershell", "-command", command], 
                     capture_output=True, 
                     text=True,
                     encoding='cp850') 

# 2. Fehlerprüfung
if ret.returncode != 0:
    print("FEHLER beim Ausführen von nmap:")
    print(ret.stderr)
else:
    # 3. Parsing
    found_ports = re.findall(r"(\d+)/tcp\s+open", ret.stdout)
    
    if not found_ports:
        print("Keine offenen Ports gefunden.")
    
    for port in found_ports:
        print(f"Gefundener Port: {port}")
        
        # Scrcpy starten
        if os.path.exists(scrcpy_path):
            print(f"Starte scrcpy für {ip}:{port} ...")
            print("Parameter: --max-size=1080 --turn-screen-off --tcpip={ip}:{port} --keyboard=uhid --mouse=uhid")
            print("INFO: Maus- & Tastatursteuerung via UHID wird verwendet. Verlassen mit LinksAlt")
            try:
                subprocess.run([
                    scrcpy_path,
                    "--max-size=1080", 
                    "--turn-screen-off", 
                    f"--tcpip={ip}:{port}",
                    "--keyboard=uhid",
                    "--mouse=uhid"
                ])                
            except Exception as e:
                print(f"Fehler beim Starten von scrcpy: {e}")
        else:
            print(f"FEHLER: scrcpy.exe nicht gefunden!")
            print(f"Sollte hier sein: {scrcpy_path}")
            print("Bitte stelle sicher, dass scrcpy.exe im selben Ordner wie die connector.exe liegt.")

print("Fertig.")
time.sleep(5)