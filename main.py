from bs4 import BeautifulSoup
import logging
import os
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

logging.basicConfig(
    format='%(asctime)s [%(levelname)5s] %(message)s', level=logging.NOTSET)


GREEN_BOX_LINK = 'https://www.getyoopi.com/product/yoopi-%d7%90%d7%a8%d7%91%d7%a2%d7%94-%d7%aa%d7%90%d7%99%d7%9d-%d7%91%d7%a6%d7%91%d7%a2-%d7%99%d7%a8%d7%95%d7%a7-%d7%aa%d7%a4%d7%95%d7%97-%d7%9e%d7%92%d7%a0%d7%98-%d7%96%d7%95%d7%92-%d7%9b%d7%a4/'
BLUE_BOX_LINK = 'https://www.getyoopi.com/product/%d7%a7%d7%95%d7%a4%d7%a1%d7%aa-yoopi-%d7%90%d7%a8%d7%91%d7%a2%d7%94-%d7%aa%d7%90%d7%99%d7%9d-%d7%9b%d7%97%d7%95%d7%9c-%d7%97%d7%9c%d7%9c/'
SECONDS_IN_HOUR = 60 * 60


def is_in_stock(link):
    logging.debug('Checking if in stock: ' + link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    return len(soup.find_all(attrs={'name': 'add-to-cart'})) > 0


def send_mail():
    print("Sending mail")
    message = Mail(
        from_email='chamuelm@gmail.com',
        to_emails='chamuelm@gmail.com',
        subject='Yoopi Stock Notifier',
        html_content='<strong>One of the products is in stock!!</strong>')

    api_key = os.environ.get('SENDGRID_API_KEY')
    if not api_key:
        error_str = 'Missing API Key'
        logging.error(error_str)
        raise Exception(error_str)

    sg = SendGridAPIClient(api_key)
    response = sg.send(message)
    logging.info('Mail Response Status Code: ' + str(response.status_code))
    logging.info('Mail Response Body: ' + str(response.body))
    logging.info('Mail Response Headers: ' + str(response.headers))


if __name__ == '__main__':
    while True:
        if is_in_stock(GREEN_BOX_LINK) or is_in_stock(BLUE_BOX_LINK):
            logging.info('Something is in stock!')
            send_mail()
            exit()

        logging.info('Nothing in stock yet, will check again in 1 hour')
        time.sleep(SECONDS_IN_HOUR)
