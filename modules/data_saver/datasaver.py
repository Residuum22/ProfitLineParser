import yaml
import codecs
from modules.utils import utils

class DataSaver():
    def __init__(self, logger_inst):
        self.logger_inst = logger_inst
        
    def read_yaml(self):
        self.logger_inst.info('Korábbi adatok beolvasása...')
        project_source_dir = utils.get_project_root()
        try:
            with codecs.open(project_source_dir / 'last_advice.yaml', 'r', encoding='utf-8') as file:
                yaml_file = file.read()
                self.logger_inst.info('KÉSZ')
                return yaml.safe_load(yaml_file)
        except:
            self.logger_inst.warning('last_advice.yaml nem létezik!')

    def compare_old_and_new_yaml(self, new_dict, old_dict):
        self.logger_inst.info('Elmentett régi adatok és új adatok komparálása...')
        for new_element in new_dict:
            for old_element in old_dict:
                if new_element['name'] == old_element['name']:
                    if new_element['status'] != old_element['status']:
                        self.logger_inst.info(f"{new_element['name']} állapota megváltozott.")
                        self.logger_inst.info(f"Régi: {old_element['status']} Új: {new_element['status']}")
        self.logger_inst.info('KÉSZ')
            
    def process_assets(self, list_of_asset):
        self.logger_inst.info('Eszközök feldolgozása...')
        for element in list_of_asset:
            del element['iterator']
            del element['link']
        self.logger_inst.info('KÉSZ')
        return list_of_asset
        
    def write_yaml(self, list_of_asset):
        self.logger_inst.info('Adatok visszaírása...')
        with codecs.open('last_advice.yaml', 'w', encoding='utf-8') as f:
            f.write(yaml.dump(list_of_asset, sort_keys=False, allow_unicode=True))
            self.logger_inst.info('KÉSZ')
            return