import os
import sys
import time
import schedule
import configparser
import requests
import yaml
import bs4
import contextlib


betas = []
bot_token = ''
chat_id = ''


def init():
    current_dir = os.path.dirname(os.path.realpath(__file__))

    global betas
    betas = parse_yaml(os.path.join(current_dir, "betas.yaml"))

    parser = configparser.ConfigParser()
    parser.read(os.path.join(current_dir, 'config.ini'))

    global bot_token, chat_id
    bot_token = parser.get('telegram_bot', 'bot_token')
    chat_id = parser.get('telegram_bot', 'chat_id')


def check_betas(always_send_result=False):
    message = ''
    if always_send_result:
        message = 'Your daily beta report:\n'

    for beta in betas:
        name = beta.get('name')
        url = beta.get('url')
        if name is None or url is None:
            continue
        html = get_html(url)
        if html is None:
            continue

        beta_available = is_beta_available(html)
        if not beta_available and not always_send_result:
            continue

        if beta_available:
            beta_status = 'available: {0}'.format(url)
            betas.remove(beta)
        else:
            beta_status = 'not available'

        message += '\nThe {0} beta is {1}.'.format(name, beta_status)

    if message != '':
        print(telegram_bot_sendtext(bot_token, chat_id, message))


def get_html(url):
    try:
        with contextlib.closing(requests.get(url, stream=True)) as resp:
            if not is_good_response(resp):
                return None
            return resp.content

    except requests.RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def is_beta_available(raw_html):
    html = bs4.BeautifulSoup(raw_html, 'html.parser')
    beta_status_containers = html.find_all('div', class_='beta-status')

    if sys.getsizeof(beta_status_containers) <= 0:
        print('Error: Unknown beta status')
        return False

    for container in beta_status_containers:
        beta_status = container.select('span')
        for span in beta_status:
            if 'To join' in span.get_text():
                return True
    return False


def parse_yaml(file):
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as er:
            print(er)
            return []


def telegram_bot_sendtext(bot_token, chat_id, message):
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    return response.json()


init()

schedule.every(1).to(3).minutes.do(check_betas)
schedule.every().day.at("09:00").do(check_betas, always_send_result=True)

while True:
    schedule.run_pending()
    time.sleep(1)
