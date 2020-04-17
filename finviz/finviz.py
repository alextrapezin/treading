from urllib.request import urlopen
from bs4 import BeautifulSoup

SOURCE_URL = 'https://finviz.com/quote.ashx?t='

def scrab(tic, keys, verbose=False):
    if len(tic) == 0:
        raise ValueError('Scrabing needs TIC')

    if verbose:
        print('get webpage from', SOURCE_URL+tic)

    response = urlopen(SOURCE_URL + tic)

    html = response.read().decode('utf8')

#    if verbose:
#        print(html)

    soup = BeautifulSoup(html, 'html5lib')

    table = soup.find('table', attrs={'class': 'snapshot-table2'})
    if len(keys) == 0:
        for td in table.find_all('td', attrs={'class': 'snapshot-td2-cp'}):
            keys.append(td.get_text())

    values = []
    for td in table.find_all('td', attrs={'class': 'snapshot-td2'}):
        values.append(td.get_text())

    for i in range(0, len(keys)):
        if keys[i] == 'Volatility':
            keys[i] = 'Volatility Week'
            keys.insert(i + 1, 'Volatility Month')
        if keys[i] == 'Volatility Week':
            v = values[i].split()
            values[i] = v[0]
            values.insert(i + 1, v[1])
    return keys, values
