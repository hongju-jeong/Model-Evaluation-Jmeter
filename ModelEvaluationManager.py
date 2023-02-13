import os
import sys

dir = os.path.realpath(__file__)
dir = os.path.abspath(os.path.join(dir,os.pardir))

sys.path.append(dir)

from DataPreprocessor import DataPreprocessor
from JmeterLauncher import JmeterLauncher
from Comparator import Comparator

class ModelEvaluationManager():
    def __init__(self):
        self.origin_file_path = ""

    def fine_origin_file(self):
        file_list = os.listdir("./faq-test-file")
        self.origin_file_path = "./faq-test-file/"+file_list[0]

    def run(self):
        self.fine_origin_file()
        data_preprocessor = DataPreprocessor(self.origin_file_path)
        file_num_list = data_preprocessor.run()
        jmeter_launcher = JmeterLauncher(file_num_list = file_num_list)
        jmeter_launcher.run()
        comparator = Comparator(file_num_list)
        comparator.run()
    
    def oneQ(self):
        self.fine_origin_file()
        data_preprocessor = DataPreprocessor(self.origin_file_path)
        file_len = data_preprocessor.one_queue_test()
        jmeter_launcher = JmeterLauncher(file_len = file_len)
        jmeter_launcher.one_queue_test()
        comparator = Comparator(file_len= file_len)
        comparator.one_queue_test()


if __name__ == "__main__":
    model_evaluation_manager = ModelEvaluationManager()
    #model_evaluation_manager.run()
    model_evaluation_manager.oneQ()