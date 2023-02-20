import os
import xml.etree.ElementTree as ET

class JmeterLauncher():
    def __init__(self, file_num_list=[], file_len=0):
        self.file_num_list = file_num_list
        self.file_len = file_len

    def mkdir_for_test(self):
        """
        response 결과를 저장하고
        원본 데이터와 비교를 진행할 디렉토리를 만든다
        """

        test_file_prefix = "./test_faq_"
        for file_num in self.file_num_list:
            os.mkdir(test_file_prefix+str(file_num))
    
    def modify_jmx_file(self,file_num):
        """
        JMeter를 실행하기 위해 필요한 jmx파일을 생성한다.
        API_test.jmx라는 템플릿이 있고
        데이터 개수별로 실행하기 위해 필요한 jmx 파일로 수정한다.

        API_test.jmx 파일에서 마지막 <Arguments>에 User Defined Variables
        이 있는데 여기는 데이터 개수를 입력하는 부분이다.
        이 부분을 수정해서 jmx파일로 만들어서 JMeter를 실행하는 것이다.
        """

        xml_path = "./API_test.jmx"
        xml_file = open(xml_path, 'rt', encoding='utf-8')

        anno = ET.parse(xml_file)
        jmeterTestPlan = anno.getroot()

        xml_file.close()

        for arguments in jmeterTestPlan.iter("Arguments"):
            if(arguments.attrib["testname"] == 'User Defined Variables'):
                for stringProp in arguments.iter("stringProp"):
                    if (stringProp.attrib["name"] == "Argument.value"):
                        stringProp.text = str(file_num)
                        break
        
        anno.write("output_"+str(file_num)+".jmx", encoding="UTF-8", xml_declaration=True)

    def launch_jmeter(self):
        """
        modify_jmx_file를 통해 만들어진 jmx 파일로 JMeter를 실행한다
        """

        for file_num in self.file_num_list:
            self.modify_jmx_file(file_num)
            os.system("./jmetercli/apache-jmeter-5.5/bin/jmeter -n -t ./output_"+str(file_num)+".jmx -l ./test_faq_"+str(file_num)+"/test_"+str(file_num)+".log")

    def run(self):
        """
        함수들을 실행한다
        """

        self.mkdir_for_test()
        self.launch_jmeter()

    def one_queue_test(self):
        """
        ModelEvaluationManager에서 oneQ 함수를 실행시킬 때 쓰는 함수로
        저기 위에 있는 모든 함수를 그대로 적었고
        데이터를 나누지않고 전체 데이터를 테스트한다.
        """
        
        test_file_prefix = "./test_faq_"
        os.mkdir(test_file_prefix+str(self.file_len))

        self.modify_jmx_file(self.file_len)
        os.system("./jmetercli/apache-jmeter-5.5/bin/jmeter -n -t ./output_"+str(self.file_len)+".jmx -l ./test_faq_"+str(self.file_len)+"/test_"+str(self.file_len)+".log")




if __name__ == "__main__":
    file_num_list = [100,500,660]
    jmeter_Launcher = JmeterLauncher(file_num_list)
    jmeter_Launcher.run()
