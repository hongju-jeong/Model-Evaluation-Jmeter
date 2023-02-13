import os
import xml.etree.ElementTree as ET

class JmeterLauncher():
    def __init__(self, file_num_list=[], file_len=0):
        self.file_num_list = file_num_list
        self.file_len = file_len

    def mkdir_for_test(self):
        test_file_prefix = "./test_faq_"
        for file_num in self.file_num_list:
            os.mkdir(test_file_prefix+str(file_num))
    
    def modify_jmx_file(self,file_num):
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
        # file_num = self.file_num_list[-1]
        # self.modify_jmx_file(file_num)
        # os.system("./jmetercli/apache-jmeter-5.5/bin/jmeter -n -t ./output_"+str(file_num)+".jmx -l ./test_faq_"+str(file_num)+"/test_"+str(file_num)+".log")
        for file_num in self.file_num_list:
            self.modify_jmx_file(file_num)
            os.system("./jmetercli/apache-jmeter-5.5/bin/jmeter -n -t ./output_"+str(file_num)+".jmx -l ./test_faq_"+str(file_num)+"/test_"+str(file_num)+".log")

    def one_queue_test(self):
        test_file_prefix = "./test_faq_"
        os.mkdir(test_file_prefix+str(self.file_len))

        self.modify_jmx_file(self.file_len)
        os.system("./jmetercli/apache-jmeter-5.5/bin/jmeter -n -t ./output_"+str(self.file_len)+".jmx -l ./test_faq_"+str(self.file_len)+"/test_"+str(self.file_len)+".log")



        

    def run(self):
        self.mkdir_for_test()
        self.launch_jmeter()




if __name__ == "__main__":
    file_num_list = [100,500,660]
    jmeter_Launcher = JmeterLauncher(file_num_list)
    jmeter_Launcher.run()
