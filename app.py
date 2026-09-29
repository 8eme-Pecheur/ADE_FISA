from datetime import datetime, timezone
import requests

# URL d'initialisation anonyme et de récupération de l'iCal ADE
ADE_ICAL_URL = "https://ade.ensea.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=579&projectId=1&calType=ical&nbWeeks=8"

def fetch_and_save_ics():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:156.0) Gecko/20100101 Firefox/156.0",
        "Accept": "*/*",
        "Accept-Language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7"
    })

    print(f"[{datetime.now(timezone.utc).isoformat()}] Fetching ADE iCal...")
    
    response = session.get(ADE_ICAL_URL, timeout=15)
    
    if response.status_code == 200 and "BEGIN:VCALENDAR" in response.text:
        with open("calendar.ics", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Fichier calendar.ics mis à jour avec succès ({len(response.text)} octets).")
    else:
        print("❌ Erreur lors de la récupération de l'iCal ADE.")
        print(response.text[:300])
        exit(1)

if __name__ == "__main__":
    fetch_and_save_ics()