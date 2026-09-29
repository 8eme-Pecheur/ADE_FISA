from datetime import datetime, timezone
import requests

# Dictionnaire associant le nom du fichier au code de ressource ADE
GROUPS = {
    "TD1": "591",
    "TD2": "579",
    "TD3": "140",
    "TD4": "142",
}

BASE_URL = "https://ade.ensea.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?projectId=1&calType=ical&nbWeeks=8&resources="


def fetch_all_calendars():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:156.0) Gecko/20100101 Firefox/156.0",
        "Accept": "*/*",
        "Accept-Language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    print(
        f"[{datetime.now(timezone.utc).isoformat()}] Début de la mise à jour des calendriers..."
    )

    for group_name, resource_id in GROUPS.items():
        url = f"{BASE_URL}{resource_id}"
        print(
            f"--> Récupération du {group_name} (resource={resource_id})..."
        )

        try:
            response = session.get(url, timeout=15)

            if (
                response.status_code == 200
                and "BEGIN:VCALENDAR" in response.text
            ):
                filename = f"{group_name}.ics"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(
                    f"  ✅ {filename} généré avec succès ({len(response.text)} octets)."
                )

                # Si c'est le TD2, on conserve aussi une copie 'calendar.ics' pour la rétrocompatibilité
                if group_name == "TD2":
                    with open("calendar.ics", "w", encoding="utf-8") as f:
                        f.write(response.text)
            else:
                print(f"  ❌ Erreur lors de la récupération pour {group_name}.")

        except Exception as e:
            print(f"  ❌ Exception pour {group_name}: {e}")


if __name__ == "__main__":
    fetch_all_calendars()