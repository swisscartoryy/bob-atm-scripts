import os
import json

from bs4 import BeautifulSoup

html_paths = [
    "assets/bcp/atms.html",
    "assets/bcp/kiosks.html",
    "assets/bcp/branches.html",
]

departmentids = [
    "fondoOficinaLaPaz",
    "fondoOficinaSantaCruz",
    "fondoOficinaOruro",
    "fondoOficinaCochabamba",
    "fondoOficinaPotosi",
    "fondoOficinaChuquisaca",
    "fondoOficinaTarija",
    "fondoOficinaTrinidad",
]

for html_path in html_paths:
    with open(html_path, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    filename = f"{html_path[len("assets/bcp/") : -len(".html")]}.json"

    for departmentid in departmentids:
        element = soup.find(id=departmentid)
        department = departmentid[len("fondooficina") :].lower()
        dirname = f"assets/bcp/{"beni" if department == "trinidad" else department}"

        os.makedirs(dirname, exist_ok=True)

        if element:
            rsrows = element.select("table > tr")
            rsheaders = element.select("table > thead > tr > th")

            rows: list[list[str]] = []
            headers = [h.get_text(strip=True) for h in rsheaders]

            for rsrow in rsrows:
                rsprops = rsrow.select("td")
                props = [rsprop.get_text(strip=True) for rsprop in rsprops]
                rows.append(props)

            drows = [dict(zip(headers, row)) for row in rows]

            json_path = f"{dirname}/{filename}"
            json_data = json.dumps(drows, ensure_ascii=False, indent=4)

            with open(json_path, "w", encoding="utf-8") as file:
                file.write(json_data)
