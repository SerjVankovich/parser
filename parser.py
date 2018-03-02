from bs4 import BeautifulSoup
import urllib.request
import json
from the_best_functions import get_float
import the_best_functions as tbf
from firebase import firebase
from del_nt import del_nt
from take_banks import take_banks

BASE_URL = 'https://www.open.ru/deposits?from=main_menu#aim14'
vklad_obj = {}
kredit_obj = {}
banks_obj = {}
all_vklads = []
all_kredits = []
firebase = firebase.FirebaseApplication('https://banx-a1b2d.firebaseio.com/')


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html, name, array):
    soup = BeautifulSoup(html, 'html.parser')
    table_titles = soup.find_all('div',
                                 class_='ui-panel-light-beige justify-grid position-relative padding-small padding-left-default padding-right-default')
    titles = []

    vklads = []
    tables_percents = soup.find_all('table', class_='standard-table')
    for table in tables_percents:
        body = table.find('tbody')
        rows = body.find_all('tr')
        stroks = []
        for row in rows:
            cols = row.find_all('td')
            stroke = []
            for col in cols:
                stroke.append(col.text)
            ok_stroke = stroke[:4]
            stroks.append(ok_stroke)

        vklads.append(stroks)

    for row in table_titles:
        title = row.find('a', class_='font-size-x-large font-bold')
        titles.append(title.text)

    for num in range(len(titles)):
        vklad = {}
        vklad['title'] = titles[num]
        vklad['bank'] = name

        for stroke in vklads[num]:
            if stroke[0] == 'Российский рубль':
                vklad['perinrub'] = str(get_float(stroke[1]))
                vklad['suminrub'] = str(get_float(stroke[2]))
                if tbf.isDay(stroke[3]):
                    vklad['srokinrub'] = str(get_float(stroke[3]))
                elif tbf.isMes(stroke[3]):
                    vklad['srokinrub'] = str(get_float(stroke[3]) * 30)
                elif tbf.isYear(stroke[3]):
                    vklad['srokinrub'] = str(get_float(stroke[3]) * 365)
                else:
                    vklad['srokinrub'] = stroke[3]
            elif stroke[0] == 'Доллар США':
                vklad['perindollars'] = str(get_float(stroke[1]))
                vklad['sumindollars'] = str(get_float(stroke[2]))
                vklad['srokindollars'] = del_nt(stroke[3])
            elif stroke[0] == 'Евро':
                vklad['perineuro'] = str(get_float(stroke[1]))
                vklad['sumineuro'] = str(get_float(stroke[2]))
                vklad['srokineuro'] = del_nt(stroke[3])
            elif stroke[0] == 'Китайский юань':
                vklad['perinuan'] = str(get_float(stroke[1]))
                vklad['suminuan'] = str(get_float(stroke[2]))
                vklad['srokinuan'] = del_nt(stroke[3])
            elif stroke[0] == 'Канадский доллар':
                vklad['perinkandol'] = str(get_float(stroke[1]))
                vklad['suminkandol'] = str(get_float(stroke[2]))
                vklad['srokinkandol'] = del_nt(stroke[3])
            elif stroke[0] == 'Австралийский доллар':
                vklad['perinaudol'] = str(get_float(stroke[1]))
                vklad['suminaudol'] = str(get_float(stroke[2]))
                vklad['srokinaudol'] = del_nt(stroke[3])
            elif stroke[0] == 'Фунт стерлингов':
                vklad['perinpound'] = str(get_float(stroke[1]))
                vklad['suminpound'] = str(get_float(stroke[2]))
                vklad['srokinpound'] = del_nt(stroke[3])
            elif stroke[0] == 'Японская иена':
                vklad['perinien'] = str(get_float(stroke[1]))
                vklad['suminien'] = str(get_float(stroke[2]))
                vklad['srokinien'] = del_nt(stroke[3])
            elif stroke[0] == 'Шведская крона':
                vklad['perinkron'] = str(get_float(stroke[1]))
                vklad['suminkron'] = str(get_float(stroke[2]))
                vklad['srokinkron'] = del_nt(stroke[3])

        array.append(vklad)


def main():
    # Parse deposits
    parse(get_html('http://www.banki.ru/products/deposits/fk_otkritie/'), 'otkritie', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/tcs/'), 'tinkoff', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/sberbank/'), 'sberbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/atb/'), 'atb', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/alfabank/'), 'alfabank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/baikalinvestbank/'), 'baikalinvestbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/bbrbank/'), 'bbrbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/binbank/'), 'binbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/v-express-bank/'), 'v-express-bank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/vtb/'), 'vtb', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/gazprombank/'), 'gazprombank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/dalnevostochny/'), 'dalnevostochny', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/mosoblbank/'), 'mosoblbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/mts-bank/'), 'mts-bank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/pochtabank/'), 'pochtabank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/primorye/'), 'primorye', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/primsotsbank/'), 'primsotsbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/ptkb/'), 'ptkb', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/promsvyazbank/'), 'promsvyazbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/rosbank/'), 'rosbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/rgsbank/'), 'rgsbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/rshb/'), 'rshb', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/roscap/'), 'roscap', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/rsb/'), 'rsb', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/sammitbank/'), 'sammitbank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/sviaz-bank/'), 'sviaz-bank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/skb-bank/'), 'skb-bank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/sovcombank/'), 'sovcombank', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/ussury/'), 'ussury', all_vklads)
    parse(get_html('http://www.banki.ru/products/deposits/homecreditbank/'), 'homecreditbank', all_vklads)

    # Parse Credits
    parse(get_html('http://www.banki.ru/products/credits/fk_otkritie/'), 'otkritie', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/tcs/'), 'tinkoff', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/sberbank/'), 'sberbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/atb/'), 'atb', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/alfabank/'), 'alfabank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/baikalinvestbank/'), 'baikalinvestbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/bbrbank/'), 'bbrbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/binbank/'), 'binbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/v-express-bank/'), 'v-express-bank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/vtb/'), 'vtb', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/gazprombank/'), 'gazprombank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/dalnevostochny/'), 'dalnevostochny', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/mosoblbank/'), 'mosoblbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/mts-bank/'), 'mts-bank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/pochtabank/'), 'pochtabank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/primorye/'), 'primorye', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/primsotsbank/'), 'primsotsbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/ptkb/'), 'ptkb', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/promsvyazbank/'), 'promsvyazbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/rosbank/'), 'rosbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/rgsbank/'), 'rgsbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/rshb/'), 'rshb', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/roscap/'), 'roscap', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/rsb/'), 'rsb', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/sammitbank/'), 'sammitbank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/sviaz-bank/'), 'sviaz-bank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/skb-bank/'), 'skb-bank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/sovcombank/'), 'sovcombank', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/ussury/'), 'ussury', all_kredits)
    parse(get_html('http://www.banki.ru/products/credits/homecreditbank/'), 'homecreditbank', all_kredits)

    vklad_obj['vklads'] = all_vklads
    kredit_obj['kredits'] = all_kredits
    banks_obj['banks'] = take_banks(all_vklads, all_kredits)
    firebase.put('', 'all_vklads', vklad_obj)
    firebase.put('', 'all_kredits', kredit_obj)
    firebase.put('', 'all_banks', banks_obj)
    print(len(all_vklads))


if __name__ == '__main__':
    main()

