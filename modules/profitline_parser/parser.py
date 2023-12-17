from bs4 import BeautifulSoup
import requests

class profit_line_parser:
    def __init__(self, logger_inst) -> None:
        self.list_of_asset = list()
        self.logger_inst = logger_inst
        
    def update_datas(self):
        # Update data from ProfitLine 
        self.logger_inst.info('Adatok gyűjtése a szerverről...')
        request = requests.get('https://profitline.hu/befektetes-biztositas/biztosito/allianz')
        soup = BeautifulSoup(request.text, 'html.parser')
        main_container = soup.find(id='main_container')
        # Get the asset funds from the list
        table = main_container.find_all('table')

        # Parse the asset funds table into text and link
        rows = BeautifulSoup(str(table), 'html.parser')
        asset_funds = rows.find_all('a')

        for i in range(len(asset_funds)):
            temporary_asset_builder = {}
            temporary_asset_builder['iterator'] = i
            temporary_asset_builder['name'] = asset_funds[i].get_text()
            temporary_asset_builder['link'] = asset_funds[i].get('href')
            temporary_asset_builder['status'] = 'null'
            self.list_of_asset.append(temporary_asset_builder)

        for i in range(len(self.list_of_asset)):
            asset_fund_req = requests.get(self.list_of_asset[i]['link'])
            parsed_asset_fund = BeautifulSoup(asset_fund_req.text, 'html.parser')

            page_useful_content = parsed_asset_fund.find('div', class_="general_box right_ajanlas_ajanlas")
            recommended_action = page_useful_content.get_text()
            
            recommended_action = recommended_action.split('\xa0')
            try:
                recommended_action = recommended_action[1]
                recommended_action_end = recommended_action.index('\r\n')
                recommended_action = recommended_action[0:recommended_action_end]
            except:
                recommended_action = "Hiba"

            self.list_of_asset[i]['status'] = recommended_action
        self.logger_inst.info('KÉSZ!')
        return

    def print_datas(self):
        for i in range(len(self.list_of_asset)):
            if self.list_of_asset[i]['status'] != 'Hiba':                
                print('Eszközalap: ' + self.list_of_asset[i]['name'])
                print('Ajánlás: ' + self.list_of_asset[i]['status'])
                print('\n')
    
    def get_list_of_assets(self):
        return self.list_of_asset