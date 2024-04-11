from bs4 import BeautifulSoup
import requests


def get_offers_as_list(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    soup.encode(encoding='utf-8')
    list_of_offers = [["Position Name", "Salary", "Company", "Location"]]

    get_offers_section = soup.find(attrs={"data-test": "section-offers"})

    extracted_offers = get_offers_section.find_all(attrs={"data-test": "default-offer"})

    for offer in extracted_offers:
        position_name = offer.find(attrs={"data-test": "offer-title"}).text
        position_salary = offer.find(attrs={"data-test": "offer-salary"}).text
        position_company_name = offer.find(attrs={"data-test": "text-company-name"}).text
        position_location = offer.find(attrs={"data-test": "text-region"}).text
        list_of_offers.append([position_name, position_salary, position_company_name, position_location])
    return list_of_offers


#  The link contains query that filter offers with salary
if __name__ == '__main__':
    my_input = input()
    url = f"https://it.pracuj.pl/praca/{my_input};kw?sal=1"
    for row in get_offers_as_list(url):
        print(row)

