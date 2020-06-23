import re
import time

from goose3 import Goose
from selenium import webdriver
import pickle

from django.conf import settings


def crawl_news():
    start_date_2020 = {
        1: '1/1/2020',
        2: '2/1/2020',
        3: '3/1/2020',
        4: '4/1/2020',
        5: '5/1/2020',
        6: '6/1/2020',
        7: '7/1/2020',
        8: '8/1/2020',
        9: '9/1/2020',
        10: '10/1/2020',
        11: '11/1/2020',
        12: '12/1/2020',
    }
    end_date_2020 = {
        1: '1/31/2020',
        2: '2/28/2020',
        3: '3/31/2020',
        4: '4/30/2020',
        5: '5/31/2020',
        6: '6/30/2020',
        7: '7/31/2020',
        8: '8/31/2020',
        9: '9/30/2020',
        10: '10/31/2020',
        11: '11/30/2020',
        12: '12/31/2020',
    }

    start_date_2019 = {
        1: '1/1/2019',
        2: '2/1/2019',
        3: '3/1/2019',
        4: '4/1/2019',
        5: '5/1/2019',
        6: '6/1/2019',
        7: '7/1/2019',
        8: '8/1/2019',
        9: '9/1/2019',
        10: '10/1/2019',
        11: '11/1/2019',
        12: '12/1/2019',
    }
    end_date_2019 = {
        1: '1/31/2019',
        2: '2/28/2019',
        3: '3/31/2019',
        4: '4/30/2019',
        5: '5/31/2019',
        6: '6/30/2019',
        7: '7/31/2019',
        8: '8/31/2019',
        9: '9/30/2019',
        10: '10/31/2019',
        11: '11/30/2019',
        12: '12/31/2019',
    }
    start_date = [start_date_2019, start_date_2020]
    end_date = [end_date_2019, end_date_2020]
    end_month = [12, 5]

    year_dict = {
        0: '2019',
        1: '2020'
    }

    regex = re.compile('[가-힣]+')

    driver = webdriver.Chrome(settings.BASE_DIR + '/core/chromedriver/')
    driver.get('https://www.google.com/search?q=korea&safe=active&sxsrf=ALeKk016rSsqlkVgxoMg8G-qi9SrpIIDFQ:1592119370797&source=lnms&tbm=nws&sa=X&ved=2ahUKEwj73qTs4oDqAhUPqpQKHb4OB10Q_AUoAnoECBgQBA&biw=1533&bih=769')
    time.sleep(0.5)

    appbar = driver.find_element_by_class_name('appbar')
    appbar = appbar.find_element_by_id('extabar')
    appbar = appbar.find_element_by_tag_name('div')
    appbar = appbar.find_element_by_class_name('WE0UJf')
    appbar = appbar.find_element_by_id('Rzn5id')
    appbar = appbar.find_element_by_tag_name('div')
    button = appbar.find_element_by_xpath('//a[text()="Change to English"]')
    button.click()
    # search 'koera' and change it to english
    time.sleep(0.5)

    top_nav = driver.find_element_by_id('top_nav')
    button = top_nav.find_element_by_xpath('//a[text()="Tools"]')
    button.click()
    time.sleep(0.1)

    g = Goose()

    for year_iter in range(0, 1):
        for i in range (10,11):
            total_script = ''
            file_name = './' + year_dict[year_iter] + '/' +str(i) + '.txt'
            sem_dir = './' + year_dict[year_iter] + '_sem/'

            top_nav = driver.find_element_by_id('top_nav')
            hdtvMenu = top_nav.find_element_by_id('hdtbMenus')
            hm1 = hdtvMenu.find_element_by_class_name('hdtb-mn-cont')
            hm2 = hm1.find_elements_by_tag_name('div')
            button = hm2[3]
            button.click()
            time.sleep(0.1)

            so1 = hdtvMenu.find_element_by_class_name('hdtb-mn-cont')
            so2 = so1.find_elements_by_tag_name('ul')
            button = so2[1].find_element_by_xpath('//span[text()="Custom range..."]')
            button.click()
            time.sleep(0.1)

            if1 = top_nav.find_element_by_class_name('n5Ug4b')
            if2 = if1.find_element_by_class_name('J6UZg')
            if3 = if2.find_element_by_class_name('NwEGxd')
            if4 = if3.find_element_by_class_name('T3kYXe')
            input1 = if4.find_element_by_class_name('OouJcb')
            input1.clear()
            input1.send_keys(start_date[year_iter][i])
            input2 = if4.find_element_by_class_name('rzG2be')
            input2.clear()
            input2.send_keys(end_date[year_iter][i])
            button = if4.find_element_by_xpath('//g-button[text()="Go"]')
            button.click()
            time.sleep(0.1)

            news_end = False
            news_cnt = 0
            for k in range(10):
                data_box = driver.find_element_by_id('rso')
                class_elements = data_box.find_elements_by_class_name('g')
                for class_element in class_elements:
                    element = class_element.find_element_by_class_name('gG0TJc')
                    element = element.find_element_by_tag_name('h3')
                    element = element.find_element_by_tag_name('a')
                    url = element.get_attribute('href')
                    if regex.search(element.text) == None:
                        article = g.extract(url=url)
                        total_script += article.cleaned_text

                        file_name_sem = sem_dir + str(i) + '_' + str(news_cnt) + '.txt'
                        with open(file_name_sem, "wb") as file:
                            pickle.dump(article.cleaned_text, file)
                        news_cnt += 1
                foot = driver.find_element_by_id('foot')
                tbody = foot.find_element_by_tag_name('tbody')
                td = tbody.find_elements_by_tag_name('td')
                try:
                    button = td[len(td) - 1].find_element_by_xpath('//span[text()="Next"]')
                    button.click()
                    time.sleep(0.1)
                except Exception:
                    news_end = True
            with open(file_name, "wb") as file:
                pickle.dump(total_script, file)
