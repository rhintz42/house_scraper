from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse, parse_qs

def setup_driver():
    return webdriver.Firefox()

def _find_element_by_id(driver, _id):
    return driver.find_element_by_id(_id)

def _find_element_by_name(driver, _name):
    return driver.find_element_by_name(_name)

def click_id(driver, _id):
    _find_element_by_id(driver, _id).click()

def send_text_by_el(el, text):
    el.clear()
    el.send_keys(text)

def send_text_by_id(driver, _id, text):
    textbox = _find_element_by_id(driver, _id)
    send_text_by_el(textbox, text)

def launch_tax_assessor(driver):
    driver.get('http://blue.kingcounty.com/Assessor/eRealProperty/default.aspx')

    input_box_id = 'kingcounty_gov_cphContent_checkbox_acknowledge'
    click_id(driver, input_box_id)

def get_parcel_num_by_url(driver):

    while True:
        try:
            url = driver.current_url
            query = urlparse(url).query
            parcel_num = parse_qs(query)['ParcelNbr'][0]
            break
        except:
            pass
    
    return parcel_num

def goto_property_detail(driver):
    click_id(driver, 'kingcounty_gov_cphContent_LinkButtonDetail')

def get_land_data(driver):
    land_data_id = 'kingcounty_gov_cphContent_DetailsViewLand'

    el = _find_element_by_id(driver, land_data_id)

    return el.text

def get_building_data(driver):
    building_data_id = 'kingcounty_gov_cphContent_DetailsViewResBldg'

    el = _find_element_by_id(driver, building_data_id)

    return el.text

def get_tax_historical_data(driver):
    tax_historical_data_id = 'kingcounty_gov_cphContent_GridViewTaxRoll'

    el = _find_element_by_id(driver, tax_historical_data_id)

    return el.text




def launch_property_tax_site(driver):
    driver.get('https://payment.kingcounty.gov/Home/Index?app=PropertyTaxes')

def search_tax_account_num(driver, parcel_num):
    input_field_name = 'search-real-property-input'
    search_button_id = 'search-real-property-submit'

    search_field = _find_element_by_name(driver, input_field_name)
    send_text_by_el(search_field, parcel_num)

    click_id(driver, search_button_id)

def search_by_address(driver, address, city, zipcode):
    address_textbox_id = 'kingcounty_gov_cphContent_txtAddress'
    city_textbox_id = 'kingcounty_gov_cphContent_txtCity'
    zipcode_textbox_id = 'kingcounty_gov_cphContent_txtZip'
    search_button_id = 'kingcounty_gov_cphContent_btn_SearchAddress'


    el = None
    while not el:
        try:
            el = driver.find_element_by_id(address_textbox_id)
        except:
            pass

    send_text_by_id(driver, address_textbox_id, address)
    send_text_by_id(driver, city_textbox_id, city)
    send_text_by_id(driver, zipcode_textbox_id, zipcode)

    click_id(driver, search_button_id)

def get_tax_account_num(driver):
    els = []
    while not els:
        els = driver.find_elements_by_class_name("panel-title")

    result = ''
    for el in els:
        if 'Tax account number' in el.text:
            result = el.text
            break

    if result:
        i = result.find('Tax account number')
        result = str(int(result[i::].split(':')[1]))

    return result

def get_mailing_address(driver, parcel_num):
    # Find tax_account_number
    tax_account_num = get_tax_account_num(driver)
    details_id = 'collapse%s' % tax_account_num

    el = _find_element_by_id(driver, details_id)

    result = ''
    lines = el.text.split('\n')
    for i,l in enumerate(lines):
        if 'Mailing address' in l:
            result = '%s, %s' % (lines[i+1], lines[i+2])

    return result

driver = setup_driver()
launch_tax_assessor(driver)
search_by_address(driver, '18610 4th Ave S', 'Burien', '98148')
parcel_num = get_parcel_num_by_url(driver)

goto_property_detail(driver)
land_data = get_land_data(driver)
building_data = get_building_data(driver)
tax_historical_data = get_tax_historical_data(driver)

# Switch sites
launch_property_tax_site(driver)
search_tax_account_num(driver, parcel_num)
mailing_address = get_mailing_address(driver, parcel_num)

driver.close()

# printout
print('Parcel Number: %s' % parcel_num)
print('Owner Mailing Address: %s' % mailing_address)
print(land_data)
print(building_data)
print(tax_historical_data)
