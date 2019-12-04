from sys import getsizeof
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def is_beta_available(raw_html):
    html = BeautifulSoup(raw_html, 'html.parser')
    beta_status_containers = html.find_all('div', class_='beta-status')
    
    if getsizeof(beta_status_containers) <= 0:
        print('Error: Unknown beta status')
        return False
    
    for container in beta_status_containers:
        beta_status = container.select('span')
        for span in beta_status:
            if 'To join' in span.get_text():
                return True
    return False

# VLC
page_html = simple_get('https://testflight.apple.com/join/bbyXP6Lx')

# SwiftKey
# page_html = simple_get('https://testflight.apple.com/join/yhIhAvjp')

# Whatsapp
# page_html = simple_get('https://testflight.apple.com/join/s4rTJVPb')
    
if page_html is not None:
    print(is_beta_available(page_html))
else:
    print('Error: No HTMl available')