from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from utils1 import *
import json
from pydantic import BaseModel, SecretStr 
import os
from fastapi import FastAPI, Depends
class User(BaseModel):
    username: str
    password: SecretStr


loginurl = 'https://www.amazon.in/gp/sign-in.html'
url = 'https://www.amazon.in/gp/css/order-history/ref=nav_your_account'




app = FastAPI()


@app.post("/store_credentials")
def crawler_method(user: User = Depends()):
    os.environ["USERNAME"] = user.username
    os.environ["PASSWORD"] = user.password.get_secret_value()
    username , password = "" , ""
    #driver = webdriver.Chrome("/Applications/chromedriver")
    chr_options = Options()
    options = chr_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    html_text = driver.find_element(By.ID, 'a-page').get_attribute('outerHTML')
        
    # uncomment following 

    #print(type(driver))
    # Print the HTML text
    filepath = 'signin_html.txt'
    with open(filepath,'w') as f:
        f.write(html_text)

    #enter the f1
    #enter the query_prompt_f1





    USER_QUERY = f"Can you extract all the opening tag of html file at {filepath} which contains these words 'email', 'password', 'signIn', 'login', 'phone number', 'username', 'email_id', 'email-id', 'email id','passcode' "

    prompt_f1 = \
    f'''
    def extract_opening_tags_with_class_or_id(html_text_path : str, keywords : list):
    """Given html text filepath and a list of key words it extracts the opening html tags that contain the any string element in the keywords"""
    html_string = open(html_text_path, 'r').read()
    keywords_pattern = '|'.join(keywords)
    # Regular expression to match opening tags with 'class' or 'id' attributes containing specified keywords

    User Query: {USER_QUERY}<human_end>
    '''

    function_call = query_raven(prompt_f1)
    opening_tags = eval(function_call)



    


    def login_method(signIn_id:str, password_id:str , username_id:str, driver=driver):
        """the method takes ids of signin button, password value, username value and login into the site"""
        try:
            driver.find_element(by= By.ID, value=username_id).send_keys(os.environ["USERNAME"])
            driver.find_element(by= By.ID, value=password_id).send_keys(os.environ["PASSWORD"])
            driver.find_element(by= By.ID, value=signIn_id).click()
            return driver
        except Exception as e:
            return str(e)

    question = f"""You are an expert Front End Developer who works with html and css.Can you find id of three html components:  sign in button, password and email and login using any function , given html text as follows: \n {opening_tags}"""
    prompt=\
    f"""
    User Query: {question}<human_end>
    """

    raven_prompt = build_raven_prompt([ login_method] , prompt)
    

    function_call = query_raven(raven_prompt)
    #LOGGEDIN

    #uncomment following

    driver = eval(function_call)
    #driver = login_method(signin_id, password_id, username_id , driver)
    time.sleep(2)
    # order_date = "a-column a-span3"
    # order_total = "a-column a-span2 yohtmlc-order-total"
    # order_id = "a-fixed-right-grid-col actions a-col-right"

    # order_date_class = driver.find_element(by = By.CLASS_NAME, value = order_date)
    # order_date_total = driver.find_element(by = By.CLASS_NAME, value = order_total)
    # order_id_class = driver.find_element(by = By.CLASS_NAME, value = order_id)
    
    try:
        order_dates = []
        order_prices = []
        order_ids = []
        product_names = []
        for i in range(2, 1000):
            order_month_button = 'a-autoid-1-announce'
            driver.find_element(by= By.ID, value=order_month_button).click()
            time.sleep(1)
            order_2024_button = 'time-filter_' + str(i)
            driver.find_element(by= By.ID, value=order_2024_button).click()
            time.sleep(5)
            # titles = WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.a-color-secondary.value')))
            # print(len(titles)//3)
            # for title in titles:
            #     print(title.text)


            # testing storing of order names


            # Example HTML content

            ################

            #################
            regex_pattern = r"""ORDER PLACED\n(.+\n)TOTAL(\n₹?.+\n)(.|\n)+ORDER\s#\s(.+)"""

            text_final = ''
            box_inners = driver.find_elements(By.CSS_SELECTOR, "div.a-box-inner")
            for box_inner in box_inners:
                all_children = box_inner.find_elements(By.XPATH, "./*")
                for child in all_children:
                    tag_name = child.tag_name
                    class_name = child.get_attribute('class')
                    element_id = child.get_attribute('id')
                    text_content = child.text
                    if class_name.find("a-fixed-right-grid") > -1 :
                        text_final = text_final + text_content + '\n'
                        #print(f"{text_content}")
                        matches = re.search(regex_pattern, text_content)

                        # Check if matches were found
                        if matches:
                            # Extract the desired groups
                            date = matches.group(1)
                            price = matches.group(2)
                            order_id = matches.group(4)

                            # Print the extracted groups
                            order_dates.append(date)
                            order_prices.append(price)
                            order_ids.append(order_id)
                            print(f"Date: {date}")
                            print(f"Price: {price}")
                            print(f"Order ID: {order_id}")
                        else:
                            product_name = text_content.split('\n')[0]
                            print(f"product_name: {product_name}")
                            product_names.append(product_name)
                        

                    # print(f"Tag Name: {tag_name}")
                    # print(f"Class Name: {class_name}")
                    # print(f"Element ID: {element_id}")
                    
                print("*"*100)
                # Access other properties like attributes
                # print(f"Attributes: {child.get_attribute('attr_name')}")
            #dict_product = {'order_date':order_dates, 'order_price':order_prices, 'order_id':order_ids, 'product_name':product_names }
    except:
        order_list = [
            {'order_date': order_dates[i], 'order_price': order_prices[i], 'order_id': order_ids[i], 'product_name': product_names[i]}
            for i in range(len(order_dates))
        ]

        json_product = json.dumps(order_list)

            # Write the JSON object to a file
        with open('product_data.json', 'w') as json_file:
            json.dump(json_product, json_file)
        with open('text_final.txt', 'w') as f:
            f.write(text_final)   
            # //*[@id="a-page"]/section/div/div[9]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/span

    # //*[@id="a-page"]/section/div/div[10]/div/div[1]/div/div/div/div[1]/div/div[1]/div[2]/span
        return json_product
    return order_dates

    #print(order_date_total)
    #print(order_id_class)


