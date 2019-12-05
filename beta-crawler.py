import yaml
from sys import getsizeof
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def main():
    betas = parse_yaml('betas.yaml')
    for beta in betas:
        name = beta.get('name')
        url = beta.get('url')
        if name is None or url is None:
            continue
        html = simple_get(url)
        if html is None:
            continue

        beta_available = is_beta_available(html)
        print_beta_status(name, beta_available)


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if not is_good_response(resp):
                return None
            return resp.content

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


def parse_yaml(file):
    with open(file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as er:
            print(er)
            return []


def print_beta_status(name, is_available):
    print('{0}: {1}'.format(name, is_available))


main()
