import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "https://lume.ufrgs.br"

TOTAL_PATENTS = 476
search_url = f"https://lume.ufrgs.br/discover?locale-attribute=en&rpp={TOTAL_PATENTS}&etal=0&group_by=none&page=1&sort_by=score&order=desc&querytype_0=title&query_relational_operator_0=contains&query_value_0=&querytype_1=author&query_relational_operator_1=contains&query_value_1=&querytype_10=orientador&query_relational_operator_10=contains&query_value_10=&querytype_11=acervo&query_relational_operator_11=contains&query_value_11=&querytype_12=descriptionSection&query_relational_operator_12=contains&query_value_12=&querytype_13=tipoAto&query_relational_operator_13=contains&query_value_13=&querytype_14=natureza&query_relational_operator_14=contains&query_value_14=&querytype_15=numeroAto&query_relational_operator_15=contains&query_value_15=&querytype_16=orgao&query_relational_operator_16=contains&query_value_16=&querytype_17=dataFinal&query_relational_operator_17=contains&query_value_17=&querytype_18=programa&query_relational_operator_18=contains&query_value_18=&querytype_19=entrevistado&query_relational_operator_19=contains&query_value_19=&querytype_2=subject&query_relational_operator_2=contains&query_value_2=&querytype_20=grandeArea&query_relational_operator_20=contains&query_value_20=&querytype_21=tipoDeApresentacao&query_relational_operator_21=contains&query_value_21=&querytype_22=areaTematica&query_relational_operator_22=contains&query_value_22=&querytype_23=coordenador&query_relational_operator_23=contains&query_value_23=&querytype_24=origem&query_relational_operator_24=contains&query_value_24=&querytype_25=unidade&query_relational_operator_25=contains&query_value_25=&querytype_26=status&query_relational_operator_26=contains&query_value_26=&querytype_27=curso&query_relational_operator_27=contains&query_value_27=&querytype_28=nivelAcademico&query_relational_operator_28=contains&query_value_28=&querytype_29=nivelDeEnsino&query_relational_operator_29=contains&query_value_29=&querytype_3=tipo&query_relational_operator_3=equals&query_value_3=Patente&querytype_30=tipoDeMaterial&query_relational_operator_30=contains&query_value_30=&querytype_4=dateIssued&query_relational_operator_4=contains&query_value_4=&querytype_5=dataAno&query_relational_operator_5=equals&query_value_5=&querytype_6=idioma&query_relational_operator_6=equals&query_value_6=&querytype_7=formatoArquivo&query_relational_operator_7=equals&query_value_7=&querytype_8=serie&query_relational_operator_8=contains&query_value_8=&querytype_9=authortd&query_relational_operator_9=contains&query_value_9=&query="
referer = None

data = {}
with requests.session() as s:
    s.headers.update({'referer': referer})
    r = s.get(search_url)

soup = BeautifulSoup(r.text, 'html.parser')
next_page = soup.find(class_="next-page-link")

handles = []
for tag in soup.find_all("div", class_="col-sm-9 artifact-description"):
    handle = tag.find("a").get("href")
    handles.append(handle)

base_url = "https://lume.ufrgs.br"
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(requests.get, base_url + handle, params={"show": "Full"}) for handle in handles]
    for future in as_completed(futures):
        r = future.result()
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.find("table", class_="ds-includeSet-table detailtable table table-striped table-hover")
        table_data = []
        for row in table.find_all("tr"):
            row_data = []
            for item in row.find_all("td"):
                row_data.append(item.text)
            table_data.append(row_data)
        data[r.url] = table_data

with open("result.json", "w") as f:
    json.dump(data, f, indent=4)