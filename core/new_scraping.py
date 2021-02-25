import requests
from bs4 import BeautifulSoup as sp
import csv

url = "https://www.designrush.com/agency/search-engine-optimization?page={}"


def get_data(url):
    res = requests.get(url)
    soup = sp(res.text, "lxml")
    address = soup.find("div", {"class": "full-address"}).text
    webiste = soup.find("h1", {"class": "title"}).find("a", {"class": "visit js--agency-website-link"}).attrs["href"]
    services = soup.find("ul", {"class": "services"}).find_all("li")
    founded = soup.find("div", {"class": "overview-adds--list"}).find_all("div", {"class": "overview-adds--item"})[
        -1].find("div", {"class": "overview-adds--text"}).text
    description = soup.find("div", {
        "class": "profile-overview--content mce-ready-content tab-overview--description profile-desktop-version"}).text
    socials = soup.find("div", {"class": "overview-socials--list"}).find_all("a")
    social_links = []
    for link in socials:
        social_url = link.attrs["href"]
        social_links.append(social_url)
    services_list = []
    for service in services:
        services_list.append(service.text.strip())
    return address, webiste, founded, description, social_links, services_list


csv_file = csv.writer(open("scraping.csv", "a", encoding="utf-8", newline=""))
csv_file.writerow(
    ["Title", "SubTitle", "Description", "website", "email", "phone number", "address", "number of employess",
     "hourly Price", "Price", "rating", "reviews", "social links", "services"])
for i in range(1, 94):
    print("Getting Page %s" % i)
    res = requests.get(url.format(i))
    soup = sp(res.text, "lxml")
    compaines_list = soup.find("ul", {"class": "agency-list"}).find_all("li", {
        "class": "agency-list-item js--agency-list-item"})
    for company in compaines_list[11:]:
        c_title = company.find("h3", {"class": "title"}).text
        c_link = company.find("h3", {"class": "title"}).find("a").attrs["href"]
        company_info = company.find("ul", {"class": "agency-list-item-info-meta"}).find_all("li")
        number_employees = company_info[1].text
        pricing_hr = company_info[2].text
        pricing = company_info[3].text
        try:
            subtitle = company.find("h4", {"class": "subtitle"}).text
        except:
            subtitle = ""
        contact = company.find("div", {"class": "agency-list-contact-box"}).find_all("a")
        phone_number = contact[0].attrs["title"]
        email = contact[1].attrs["title"]
        try:
            rating = company.find("span", {"class": "review-rating"}).text
            review_count = company.find("span", {"class": "review-count"}).text.split()[0].replace("(", "").strip()
        except:
            rating = ""
            review_count = ""
        address, website, founded, description, social_links, services_list = get_data(c_link)
        main_data = [c_title, subtitle, description, website, email, phone_number, address, number_employees,
                     pricing_hr, pricing, rating, review_count]
        main_data.append(",".join(social_links))
        main_data.append(",".join(services_list))
        csv_file.writerow(main_data)
        print(f"Added {c_title}")
