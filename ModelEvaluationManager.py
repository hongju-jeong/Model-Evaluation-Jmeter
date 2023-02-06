import os
import sys

dir = os.path.realpath(__file__)
dir = os.path.abspath(os.path.join(dir,os.pardir))

sys.path.append(dir)

from DataPreprocessor import DataPreprocessor
from JmeterLauncher import JmeterLauncher

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
        jmeter_launcher = JmeterLauncher(file_num_list)
        jmeter_launcher.run()


        



if __name__ == "__main__":
    model_evaluation_manager = ModelEvaluationManager()
    model_evaluation_manager.run()