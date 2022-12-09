import xml.etree.ElementTree
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import re
import xml.dom.minidom


def main():
    context = ssl._create_unverified_context()
    # Dict with xml 'category ID': ['link', 'name']
    xml_cat = {'1': ['http://all-cool.ru/bitrix/catalog_export/nal_desh_i_kabin.xml', 'Кабины в наличии'],
               '2': ['http://all-cool.ru/bitrix/catalog_export/NE_nal_desh_i_kabin.xml', 'Кабины не в наличии']
               }

    # # Dict for load from directory
    # xml_cat = {'1': ['nal_desh_i_kabin.xml', 'Кабины в наличии'],
    #            '2': ['NE_nal_desh_i_kabin.xml', 'Кабины не в наличии']
    #            }

    results = []
    for i in xml_cat:
        # For load from website
        req = Request(
            url=xml_cat[i][0],
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req, context=context).read().decode('UTF-8')

        # # for load from directory
        # with open('../' + xml_cat[i][0], 'r') as file:
        #     webpage = file.read()

        soup = bs(webpage, features="xml")
        start_date = soup.find('yml_catalog').attrs
        offers = soup.find_all('offer')
        if i == '1':
            results.append([re.sub('<categoryId>\d+</categoryId>', '<categoryId>1</categoryId>', i.__str__()) for i in offers])
        if i == '2':
            results.append([re.sub('<categoryId>\d+</categoryId>', '<categoryId>2</categoryId>', i.__str__()) for i in offers])

    # Begin XML
    start = f'<yml_catalog date="{start_date["date"]}"><shop><name>all-cool.ru</name><company>all-cool.ru</company><url>http://all-cool.ru</url><platform>BSM/Yandex/Market</platform><version>2.3.0</version><cpa>1</cpa><currencies><currency id="RUR" rate="1"/></currencies><categories><category id="1">В наличии</category><category id="2">Не в наличии</category></categories><enable_auto_discounts>true</enable_auto_discounts><offers>'

    # End XML
    end = '</offers></shop></yml_catalog>'

    # Offers XML
    data = start + ''.join(results[0]) + ''.join(results[1]) + end

    def beautify_xml(xml_str):
        dom = xml.dom.minidom.parseString(xml_str)
        return dom.toprettyxml()

    with open('data2.xml', 'wt') as fout:
        fout.write(beautify_xml(data))

    print(f'XML was created\n'
          f'В наличии - {len(results[0])}\n'
          f'Не в наличии - {len(results[1])}')


if __name__ == '__main__':
    main()
