import os
import re

import json
import inflection

from bs4 import BeautifulSoup

transvowels = str.maketrans(
    "áéíóúÁÉÍÓÚ",
    "aeiouAEIOU",
)

htmlfiles = [
    "assets/bcp/atms.html",
    "assets/bcp/kiosks.html",
    "assets/bcp/branches.html",
]

departmentids = [
    "fondoOficinaLaPaz",
    "fondoOficinaOruro",
    "fondoOficinaPotosi",
    "fondoOficinaTarija",
    "fondoOficinaTrinidad",
    "fondoOficinaSantaCruz",
    "fondoOficinaCochabamba",
    "fondoOficinaChuquisaca",
]


for htmlfile in htmlfiles:
    with open(htmlfile, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    filename = f"{htmlfile[len("assets/bcp/") : -len(".html")]}.json"

    for departmentid in departmentids:
        element = soup.find(id=departmentid)
        department = departmentid[len("fondooficina") :].lower()
        dirname = f"assets/bcp/{"beni" if department == "trinidad" else department}"

        os.makedirs(dirname, exist_ok=True)

        if element:
            rsrows = element.select("table > tr")
            rsheaders = element.select("table > thead > tr > th")

            headers = [
                inflection.camelize(
                    uppercase_first_letter=False,
                    string=h.get_text(strip=True)
                    .replace(" ", "_")
                    .translate(transvowels),
                )
                for h in rsheaders
            ]

            rows = [
                [
                    re.sub(r"\s+", " ", rsprop.get_text(strip=True))
                    for rsprop in rsrow.select("td")
                ]
                for rsrow in rsrows
            ]

            drows = [dict(zip(headers, row)) for row in rows]

            filename = f"{dirname}/{filename}"
            json_data = json.dumps(drows, ensure_ascii=False, indent=4)

            with open(filename, "w", encoding="utf-8") as jsonfile:
                jsonfile.write(json_data)
