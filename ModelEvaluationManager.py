import os
import sys

dir = os.path.realpath(__file__)
dir = os.path.abspath(os.path.join(dir,os.pardir))

sys.path.append(dir)

from DataPreprocessor import DataPreprocessor
from JmeterLauncher import JmeterLauncher
from Comparator import Comparator

class ModelEvaluationManager():
    """
    DataPreprocessor, JmeterLauncher, Comparator를 연결하는 클래스

    run은 데이터를 100개, 500개, 1000개로 테스트하기위한 함수이고,
    oneQ는 데이터 전체를 그 개수 만큼 한번 테스트 함
    그래서 if __name__ == "__main__"에서 둘 중 하나 선택해서 테스트하면 됨

    실행 전 
    ./faq.json 처럼 데이터를 받는다면 
    ./json2csv.ipynb를 통해
    ./faq-test-file에 csv파일로 변환해 데이터를 넣어줘야 한다.
    ./faq-test-file에는 csv파일이 하나만 있어야 한다.

    실행 후 생기는
    ./faq_xxx 디렉토리
    ./result 디렉토리
    ./separate_faq_xxx 디렉토리
    ./test_faq_xxx 디렉토리
    ./output_xxx.jmx 파일
    은 지워준다.
    """

    def __init__(self):
        self.origin_file_path = ""

    def find_origin_file(self):
        """
        ./faq-test-file에서 질문과 답변으로 구성된 csv파일을 찾아서
        경로를 저장
        """

        file_list = os.listdir("./faq-test-file")
        self.origin_file_path = "./faq-test-file/"+file_list[0]

    def run(self):
        """
        DataPreprocessor, JmeterLauncher, Comparator를 차례로 실행
        (100개, 500개, 1000개 버전)

        ※사실 데이터 개수가 500개 이상 이어야 한다
        밑에 oneQ는 개수 상관 없음

        """

        self.find_origin_file()
        data_preprocessor = DataPreprocessor(self.origin_file_path)
        file_num_list = data_preprocessor.run()
        jmeter_launcher = JmeterLauncher(file_num_list = file_num_list)
        jmeter_launcher.run()
        comparator = Comparator(file_num_list)
        comparator.run()
    
    def oneQ(self):
        """
        DataPreprocessor, JmeterLauncher, Comparator를 차례로 실행
        (데이터 전체 버전)
        """
        self.find_origin_file()
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