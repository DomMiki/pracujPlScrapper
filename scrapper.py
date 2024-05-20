from bs4 import BeautifulSoup
import openpyxl
import requests
import csv
import os
import datetime


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


def get_position_keywords_for_search(excel_path=ROOT_PATH + "\PracujPl.xlsm", sheet="InputData", table_name="Tabela3"):
    positions_to_process = []
    workbook = openpyxl.load_workbook(excel_path)
    worksheet = workbook[sheet]
    excel_table_range = worksheet.tables[table_name].ref
    excel_position_names = worksheet[excel_table_range]
    for cell_obj in excel_position_names[1:]:  # slice the list to skip first item
        for cell_value in cell_obj:
            positions_to_process.append(cell_value.value)
    return positions_to_process


def get_offers_as_list(url, dateformat="%d.%m.%Y"):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    #  soup.encode(encoding='utf-8')
    list_of_offers = []
    get_offers_section = soup.find(attrs={"data-test": "section-offers"})
    extracted_offers = get_offers_section.find_all(attrs={"data-test": "default-offer"})

    for offer in extracted_offers:
        try:
            position_name = offer.find(attrs={"data-test": "offer-title"}).text
            position_location = offer.find(attrs={"data-test": "text-region"}).text
            position_company_name = offer.find(attrs={"data-test": "text-company-name"}).text
            position_experience = offer.find(attrs={"data-test": "offer-additional-info-0"}).text
            position_working_hours = offer.find(attrs={"data-test": "offer-additional-info-1"}).text
            position_contract_type = offer.find(attrs={"data-test": "offer-additional-info-2"}).text
            position_opareting_mode = offer.find(attrs={"data-test": "offer-additional-info-3"}).text
        except Exception:
            print("One of the offers can't be added due to incorrect HTML structure")
            continue

        try:
            position_salary = offer.find(attrs={"data-test": "offer-salary"}).text
        except Exception:
            position_salary = "-"

        list_of_offers.append([position_name,
                               position_location,
                               position_company_name,
                               position_salary,
                               position_experience,
                               position_working_hours,
                               position_contract_type,
                               position_opareting_mode,
                               datetime.date.today().strftime(dateformat)])
    return list_of_offers


def write_scrapp_csv(data_to_write, filename=ROOT_PATH + "\python_output.csv", headers=["NazwaStanowiska", "Miejscowość", "Firma", "PLN", "Doświadczenie", "RodzajUmowy", "RodzajKontraktu", "TrybPracy", "DataPobrania"]):
    with open(filename, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data_to_write)


#  The link contains query that filter offers with salary
if __name__ == '__main__':

    try:
        os.remove("python_output.csv")
    except:
        print("No file to delete!")

    position_keywords = get_position_keywords_for_search()
    for position_keyword in position_keywords:
        url = f"https://it.pracuj.pl/praca/{position_keyword};kw"
        data = get_offers_as_list(url)
        write_scrapp_csv(data)

