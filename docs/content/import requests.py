import requests
from bs4 import BeautifulSoup
import difflib
import re
import unicodedata
from urllib.parse import quote, urljoin

BASE_URL = "https://www.assettoworld.com"
SEARCH_URL_TEMPLATE = "https://www.assettoworld.com/cars/search?q={query}&sort=recent"


def normalize_text(text):
    """Normalise une chaîne pour mieux comparer (accents, maj/min…)."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().strip()
    return text


def search_car_url(query):
    """
    Recherche une voiture sur le site avec un nom approximatif
    et renvoie l'URL de la meilleure correspondance (ou None).
    """
    q = quote(query)
    search_url = SEARCH_URL_TEMPLATE.format(query=q)
    resp = requests.get(search_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    candidates = []

    # 💡 On prend tous les liens qui ressemblent à des pages voiture (/car/...)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)
        if "/car/" in href and title:
            full_url = urljoin(BASE_URL, href)
            candidates.append((title, full_url))

    if not candidates:
        return None

    # Comparaison floue entre la requête et les titres de voitures
    query_norm = normalize_text(query)
    names_norm = [normalize_text(title) for title, _ in candidates]

    best_names = difflib.get_close_matches(query_norm, names_norm, n=1, cutoff=0.0)
    if not best_names:
        return None

    best_norm = best_names[0]
    best_index = names_norm.index(best_norm)
    best_title, best_url = candidates[best_index]

    print(f"👍 Meilleure correspondance trouvée : {best_title} -> {best_url}")
    return best_url


def get_car_specs(car_url):
    """
    Scrape la page d'une voiture et renvoie :
    {year, power_bhp, torque_nm, top_speed_kmh}
    """
    resp = requests.get(car_url)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    # Essayer de récupérer le bloc "Details"
    details_text = ""
    for tag in soup.find_all(["h2", "h3", "h4", "h5"]):
        if "Details" in tag.get_text():
            details_text = tag.parent.get_text(" ", strip=True)
            break

    if not details_text:
        details_text = soup.get_text(" ", strip=True)

    # Normalisation
    details_text = unicodedata.normalize("NFKD", details_text)
    details_text = re.sub(r"\s+", " ", details_text)

    patterns = {
        "year": r"Year:\s*([0-9]{4})",
        "power_bhp": r"Power:\s*([0-9]+)\s*bhp",
        "torque_nm": r"Torque:\s*([0-9]+)\s*Nm",
        "top_speed_kmh": r"Top Speed:\s*([0-9]+)\s*km/h",
    }

    data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, details_text, flags=re.IGNORECASE)
        if match:
            try:
                data[field] = int(match.group(1))
            except ValueError:
                data[field] = match.group(1)
        else:
            data[field] = None

    return data


def main():
    user_query = input("Nom de la voiture : ")

    car_url = search_car_url(user_query)
    if not car_url:
        print("❌ Aucune voiture trouvée pour cette recherche.")
        return

    specs = get_car_specs(car_url)

    print("\nRésultat :")
    print(f"Année       : {specs['year']}")
    print(f"Puissance   : {specs['power_bhp']} bhp" if specs['power_bhp'] else "Puissance   : N/A")
    print(f"Couple      : {specs['torque_nm']} Nm" if specs['torque_nm'] else "Couple      : N/A")
    print(f"Vitesse max : {specs['top_speed_kmh']} km/h" if specs['top_speed_kmh'] else "Vitesse max : N/A")


if __name__ == "__main__":
    main()

