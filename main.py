from asyncio.windows_events import NULL
from cgitb import html
from ctypes import sizeof
from os import link
from bs4 import BeautifulSoup
import requests

class asset_funds_storage:
    def __init__(self) -> None:
        self.name = list()
        self.link = list()
        self.status = list()

    def add_name(self, name):
        self.name.append(name)

    def add_link(self, link):
        self.link.append(link)

    def add_status(self, status):
        self.status.append(status)


    
class profit_line_parser:
    def __init__(self) -> None:
        self.storage = asset_funds_storage()
        pass
        

    def update_datas(self):
        # Update data from ProfitLine 
        request = requests.get('https://profitline.hu/befektetes-biztositas/biztosito/allianz')
        soup = BeautifulSoup(request.text, 'html.parser')
        main_container = soup.find(id='main_container')
        # Get the asset funds from the list
        table = main_container.find_all('table')

        # Parse the asset funds table into text and link
        rows = BeautifulSoup(str(table), 'html.parser')
        asset_funds = rows.find_all('a')

        for element in asset_funds:
            self.storage.add_name(element.get_text())
            self.storage.add_link(element.get('href'))
        
        for i in range(len(self.storage.link)):
            asset_fund_req = requests.get(self.storage.link[i])
            parsed_asset_fund = BeautifulSoup(asset_fund_req.text, 'html.parser')

            page_useful_content = parsed_asset_fund.find('div', class_="general_box right_ajanlas_ajanlas")
            recommended_action = page_useful_content.get_text()
            
            recommended_action = recommended_action.split('\xa0')
            recommended_action = recommended_action[1]
            recommended_action_start = 0
            recommended_action_end = recommended_action.index('\r\n')
            recommended_action = recommended_action[recommended_action_start:recommended_action_end]

            self.storage.add_status(recommended_action)
        return

    def print_datas(self):
        for i in range(len(self.storage.name)):
            print(f'Eszközalap: {self.storage.name[i]}')
            print(f'Ajánlás: {self.storage.status[i]}')
            if self.storage.status[i] == 'Vétel':
                print('🟩🟩🟩🟩🟩🟩')
            elif self.storage.status[i] == 'Tartás':
                print('🟨🟨🟨🟨🟨🟨')
            else:
                print('🟥🟥🟥🟥🟥🟥')
            print
            print('\n')
        

if __name__ == "__main__":
    asd = profit_line_parser()
    asd.update_datas()
    asd.print_datas()
    exit()