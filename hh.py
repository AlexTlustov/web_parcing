import json
import bs4 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def get_list_url():
    list_url = []
    for i in range(0, 5):
        url = f'https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python+django+flask&search_field=description&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&page={i}'
        list_url.append(url)
    return list_url
    
def get_info(list_url):
    list_data = []
    for url in list_url:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        main_soup = bs4.BeautifulSoup(driver.page_source, 'lxml')
        all_jobs = main_soup.find_all(class_ = 'serp-item')
        for job in all_jobs:
            vacansy_blog = job.find('div', class_ = 'vacancy-serp-item-body__main-info')
            h3_tag = vacansy_blog.find('h3', class_ = 'bloko-header-section-3')
            link_job = h3_tag.find('a')['href']
            tittle_job = h3_tag.text
            salary = vacansy_blog.find('span', class_ = 'bloko-header-section-3')
            if salary is None:
                text_salary = 'Не указана.'
            else:
                text_salary = salary.text
            about_organization = vacansy_blog.find('div', class_ = 'vacancy-serp-item-company') 
            text_organization = about_organization.find('a').text
            city_vacansy = vacansy_blog.find('div', class_ = 'vacancy-serp-item__info')
            about_adres = about_organization.find_all(class_ = 'bloko-text')
            text_city = about_adres[1].text
            list_data.append({
                'link': link_job,
                'name_job': tittle_job,
                'salary': text_salary,
                'name_company': text_organization,
                'city': text_city
            })
    return list_data

final_list_data = get_info(get_list_url())
with open('all_jobs_HH.RU.json', 'w', encoding='utf-8') as f:
    json.dump(final_list_data, f, ensure_ascii=False)

    

