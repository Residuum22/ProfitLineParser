from modules.profitline_parser import parser
from modules.data_saver import datasaver

import logging
from modules.logger import logger

def init_logger():
    # create logger with 'spam_application'
    app_logger = logging.getLogger("ProfitLineParser")
    app_logger.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logger.CustomFormatter())
    app_logger.addHandler(ch)
    return app_logger

if __name__ == "__main__":
    logger_inst = init_logger()

    parser_instance = parser.profit_line_parser(logger_inst)
    parser_instance.update_datas()
    # parser_instance.print_datas()
    datasaver_inst = datasaver.DataSaver(logger_inst)
    new_json = datasaver_inst.process_assets(parser_instance.get_list_of_assets())
    
    json_file = datasaver_inst.read_yaml()
    if json_file != None:
        datasaver_inst.compare_old_and_new_yaml(new_dict=new_json, old_dict=json_file)

    datasaver_inst.write_yaml(new_json)
    exit()