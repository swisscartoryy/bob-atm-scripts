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

departmentidname: dict[str, str] = {
    "fondoOficinaOruro": "oruro",
    "fondoOficinaLaPaz": "la_paz",
    "fondoOficinaPotosi": "potosi",
    "fondoOficinaTarija": "tarija",
    "fondoOficinaTrinidad": "beni",
    "fondoOficinaSantaCruz": "santa_cruz",
    "fondoOficinaCochabamba": "cochabamba",
    "fondoOficinaChuquisaca": "chuquisaca",
}

for htmlfile in htmlfiles:
    with open(htmlfile, "r", encoding="utf-8") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    filename = f"{htmlfile[len("assets/bcp/") : -len(".html")]}.json"

    for departmentid in departmentidname.keys():
        element = soup.find(id=departmentid)
        dirname = f"assets/bcp/{departmentidname[departmentid]}"

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

            jfilename = f"{dirname}/{filename}"
            json_data = json.dumps(drows, ensure_ascii=False, indent=4)

            with open(jfilename, "w", encoding="utf-8") as jsonfile:
                jsonfile.write(json_data)
