import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver_path = "chromedriver_win32/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(executable_path=driver_path, options=options)



def getcsv(current_url, lol):
    driver.get(current_url)
    sleep(3)
    print("i have awoken")
    # csv_butt = driver.find_element_by_xpath("//*[text()='Get table as CSV (for Excel)']")
    # csv_butt.click()
    driver.execute_script("window.scrollTo(0, 400)") 
    a = ActionChains(driver)
    m = driver.find_element_by_xpath("//*[text()='Share & Export']")
    a.move_to_element(m).perform()
    # driver.implicitly_wait(1)
    sleep(2)
    n = driver.find_element_by_xpath("//*[text()='Get table as CSV (for Excel)']")
    a.move_to_element(n).click().perform()

    csv_stuff = driver.find_element_by_id("csv_" + lol + "_stats")
    stats_list = str(csv_stuff.text).split('\n')

    return stats_list[4:]

stat = str(sys.argv[1])
year = 1980
while year <= 2021:
    filepath = "./" + stat + "_stats/" + str(year) + stat + "_stats.csv"
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_" + stat + ".html"
    stats_list = getcsv(url, stat)
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        headers = stats_list.pop(0).split(',')
        writer.writerow(headers)

        for row in stats_list:
            writer.writerow(row.split(','))
    year += 1

driver.close()
