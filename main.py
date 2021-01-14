from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import datetime
import re

driver = webdriver.Chrome()
driver.maximize_window()

URL = "https://portalsistemas.ipasgo.go.gov.br/SAAT/login.asp"

today = datetime.date.today()


def site_login():

    driver.get(URL)
    driver.find_element_by_id("txtMatricula").send_keys("12275080")
    driver.find_element_by_id("txtSenha").send_keys("6317Crd")
    driver.find_element_by_name("botao_entrar").click()


def open_history_guias():
    driver.get(
        "https://portalsistemas.ipasgo.go.gov.br/SAAT/GuiasEmitidasCanceladas.asp")

    driver.find_element_by_id("txtDataInicial").send_keys(
        today.strftime('%d/%m/%Y'))
    driver.find_element_by_id("txtDataFinal").send_keys(
        today.strftime('%d/%m/%Y'))

    driver.execute_script("javascript:emitirRelatorio()")


def iterate_table_history_guias():
    mylist = []

    table = driver.find_element_by_xpath(
        "//table[@class='RelLinhaBranca']/tbody/tr[@class='FormTitulo']")
    for td in table.find_elements_by_xpath("//td[@class='RelLinhaBranca' or @class='RelLinhaCinza'][1]"):
        mylist.append(re.sub('[^0-9]', '', td.text))

    mylist.pop(0)
    return mylist


def iterate_guias(nr_guias):

    driver.get(
        "https://portalsistemas.ipasgo.go.gov.br/SAAT/Reimpressao_Prestador.asp")

    for guia in nr_guias:

        driver.find_element_by_id("txtNumrSolicitacao").send_keys(guia)
        driver.execute_script("javascript:emitirRelatorio()")

        driver.switch_to.window(driver.window_handles[2])

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'relatorio')))

        except TimeoutException:
            pass  # Handle the exception here

        for elem in driver.find_elements_by_xpath(".//span[@class='relatorio' or @class='relatoriop']"):
            print(elem.text)

        # driver.close()
        # driver.switch_to.window(driver.window_handles[3])

        driver.get(
            "https://portalsistemas.ipasgo.go.gov.br/SAAT/Reimpressao_Prestador.asp")


'''
        for elem in driver.find_elements_by_xpath(".//span[@class='relatorio' or @class='relatoriop']"):
            print(elem.text)
            '''


# driver.switch_to.window(window_before)


site_login()
window_before = driver.window_handles[0]

open_history_guias()
window_after = driver.window_handles[1]

driver.switch_to.window(window_after)

nr_guias = iterate_table_history_guias()

print(nr_guias)


iterate_guias(nr_guias)

driver.quit()


# driver.close()


# table = driver.find_element_by_class_name('FormTitulo')

# print(driver.find_element_by_xpath("//table[3]/tbody/tr[1]/td[1]").text)


'''try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'gvContractors')))
except TimeoutException:
    pass  # Handle the exception here
main_table = driver.find_elements_by_tag_name('table')
outer_table = main_table[3].find_element_by_tag_name('table')
print(outer_table.get_attribute('innerHTML'))
'''

# driver.quit()
