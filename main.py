from bs4 import BeautifulSoup
import requests
import json

class profit_line_parser:
    def __init__(self) -> None:
        self.list_of_asset = list()
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
        return

    def print_datas(self):
        for i in range(len(self.list_of_asset)):
            if self.list_of_asset[i]['status'] != 'Hiba':                
                print('Eszközalap: ' + self.list_of_asset[i]['name'])
                print('Ajánlás: ' + self.list_of_asset[i]['status'])
                print('\n')
    
    def get_list_of_assets(self):
        return self.list_of_asset
        
def read_json():
    try:
        with open('last_advice.json', 'r') as f:
            json_file = f.read()
            return json.loads(json_file)
    except:
        print('WARNING: last_advice.json nem létezik.')

def compare_old_and_new_json(new_json, old_json):
    for new_element in new_json:
        for old_element in old_json:
            if new_element['name'] == old_element['name']:
                if new_element['status'] != old_element['status']:
                    print(f"{new_element['name']} állapota megváltozott.")
                    print(f"Régi: {old_element['status']} Új: {new_element['status']}")
        
def process_json(list_of_asset):
    for element in list_of_asset:
        del element['iterator']
        del element['link']
    return list_of_asset

def write_json(list_of_asset):
    with open('last_advice.json', 'w') as f:
        f.write(json.dumps(list_of_asset))
        return

if __name__ == "__main__":
    parser_instance = profit_line_parser()
    parser_instance.update_datas()
    # parser_instance.print_datas()
    new_json = process_json(parser_instance.get_list_of_assets())
    
    json_file = read_json()
    if json_file != None:
        compare_old_and_new_json(new_json=new_json, old_json=json_file)
        
    write_json(new_json)
    exit()