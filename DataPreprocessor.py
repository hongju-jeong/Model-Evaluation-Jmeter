import pandas as pd
import os
import random
import json
from collections import OrderedDict
import copy

class DataPreprocessor():
    def __init__(self, _origin_file_path):
        self.origin_file_path = _origin_file_path

    def check_amount_of_items_origin_file(self):
        """
        csv 파일 데이터 개수 리턴
        """

        df_faq = pd.read_csv(self.origin_file_path, sep = ',', encoding='utf-8')
        return len(df_faq)

    def make_separate_faq_dir(self, file_len):
        """
        100개, 500개, 1000개를 나눠서 저장할
        디렉토리 생성 후 file_number_list에 100,500,1000 저장 후 리턴
        
        500개 이상 1000개 미만이면 file_number_list의 마지막 수는
        데이터 전체 개수다.

        ex) 1500개
        file_number_list = [100,500,1000]

        ex) 700개
        file_number_list = [100,500,700]

        """

        file_number_list= []
        if(file_len < 1000):
            os.mkdir("separate_faq_100")
            file_number_list.append(100)
            os.mkdir("separate_faq_500")
            file_number_list.append(500)
            os.mkdir("separate_faq_"+ str(file_len))
            file_number_list.append(file_len)

        else:
            os.mkdir("separate_faq_100")
            file_number_list.append(100)
            os.mkdir("separate_faq_500")
            file_number_list.append(500)
            os.mkdir("separate_faq_1000")
            file_number_list.append(1000)

        return file_number_list
    
    def random_extract_data(self, file_num_list):
        """
        csv 파일을 file_number_list에 맞게 랜덤으로 데이터를 추출해
        csv 파일로 separate_faq_xxx 폴더에 넣는다.
        """

        df_faq = pd.read_csv(self.origin_file_path, sep = ',', encoding='utf-8')

        last_file_number = 0

        _file_num_list = copy.deepcopy(file_num_list)

        if(len(df_faq)<1000):
            last_file_number = _file_num_list.pop()

        for file_number in _file_num_list:
            df_output_question = pd.DataFrame(columns=("question", "answer"))
            random_number_list = []
            i = 0
            while(i<file_number):
                random_number = random.randrange(0,len(df_faq))
                if random_number in random_number_list:
                    continue
                else :
                    random_number_list.append(random_number)
                    df_output_question.loc[i] = df_faq.loc[random_number]
                    i+=1
            
            file_name = "./separate_faq_"+str(file_number)+"/faq_"+str(file_number)+".csv"
            df_output_question.to_csv(file_name, index=False, encoding='utf-8-sig')

        if(len(df_faq)<1000):
            file_name = "./separate_faq_"+str(last_file_number)+"/faq_"+str(last_file_number)+".csv"
            df_faq.to_csv(file_name, index=False, encoding='utf-8-sig')

    def separate_to_json(self, file_num_list):
        """
        random_extract_data에 의해 나뉜 csv파일 각각 한줄씩 모두
        json파일로 만들고 압축한다.
        """

        for file_num in file_num_list:
            file_path = "./separate_faq_"+str(file_num)
            df = pd.read_csv(file_path+'/faq_'+str(file_num)+'.csv', sep=',', encoding='utf-8')

            index_file_data = OrderedDict()

            for i in range(len(df)):
                make_file = open(file_path+'/'+str(i)+'.json', 'w', encoding='utf-8')
                index_file_data["sender"] = str(i)
                index_file_data["message"] = str(df.iat[i,0])
                json.dump(index_file_data,make_file,ensure_ascii=False)
                make_file.close()

            os.system("zip "+file_path+"/faq_"+str(file_num)+".zip "+file_path+"/*.json")
            os.system("rm "+file_path+"/*.json")

    def mkdir_for_test(self, file_num_list):
        """
        separate_to_json에 의해 나뉜 json파일를 보관할 디렉토리를 만든다.
        """

        file_path_prefix = "./faq_"
        for file_num in file_num_list:
            os.mkdir(file_path_prefix+str(file_num))

    def unzip_faq_data(self, file_num_list):
        """
        separate_to_json에 압축된 json 파일들을 
        mkdir_for_test에 의해 생성된 폴더에 압축을 해제한다.
        """

        origin_file_path_prefix = "./separate_faq_"
        destination_file_path_prefix = "./faq_"

        for file_num in file_num_list:
            os.system("unzip "+origin_file_path_prefix+str(file_num)+"/faq_"+str(file_num)+".zip -d "+destination_file_path_prefix+str(file_num))

    def make_csv_for_index(self, file_num_list):
        """
        JMeter로 여러 json을 보내기 위해서는 그 json 파일 개수 만큼
        인덱스를 가지고 있는 csv 파일이 하나 필요하다.

        json파일이 3개이면 

        1
        2
        3

        이렇게 인덱스가 있는 csv파일을 json과 같은 폴더에 넣어준다.

        """

        first_file_path_prefix = "./faq_"
        second_file_path_prefix = "/separate_faq_"

        for file_num in file_num_list:
            file_path = first_file_path_prefix+str(file_num)+second_file_path_prefix+str(file_num)+"/Json.csv"
            file = open(file_path, 'w', encoding='utf-8')

            for i in range(file_num):
                file.write(str(i))
                if(i < file_num-1):
                    file.write('\n')

            file.close()

    



    def run(self):
        """
        함수들을 차례대로 실행시켜 준다.

        file_num_list를 리턴한다.
        """

        file_len = self.check_amount_of_items_origin_file()
        print(file_len)
        file_num_list = self.make_separate_faq_dir(file_len)
        self.random_extract_data(file_num_list)
        self.separate_to_json(file_num_list)
        self.mkdir_for_test(file_num_list)
        self.unzip_faq_data(file_num_list)
        self.make_csv_for_index(file_num_list)

        return file_num_list

    def one_queue_test(self):
        """
        ModelEvaluationManager에서 oneQ 함수를 실행시킬 때 쓰는 함수로
        저기 위에 있는 모든 함수를 그대로 적었고
        데이터를 나누지않고 전체 데이터를 테스트한다.

        데이터의 개수를 의미하는 file_len을 리턴한다.
        """

        file_len = self.check_amount_of_items_origin_file()
        os.mkdir("separate_faq_"+ str(file_len))
        df_faq = pd.read_csv(self.origin_file_path, sep = ',', encoding='utf-8')
        file_name = "./separate_faq_"+str(file_len)+"/faq_"+str(file_len)+".csv"
        df_faq.to_csv(file_name, index=False, encoding='utf-8-sig')

        file_path = "./separate_faq_"+str(file_len)
        df = pd.read_csv(file_path+'/faq_'+str(file_len)+'.csv', sep=',', encoding='utf-8')

        index_file_data = OrderedDict()

        for i in range(len(df)):
            make_file = open(file_path+'/'+str(i)+'.json', 'w', encoding='utf-8')
            index_file_data["sender"] = str(i)
            index_file_data["message"] = str(df.iat[i,0])
            json.dump(index_file_data,make_file,ensure_ascii=False)
            make_file.close()

        os.system("zip "+file_path+"/faq_"+str(file_len)+".zip "+file_path+"/*.json")
        os.system("rm "+file_path+"/*.json")

        file_path_prefix = "./faq_"
        os.mkdir(file_path_prefix+str(file_len))

        origin_file_path_prefix = "./separate_faq_"
        destination_file_path_prefix = "./faq_"
        os.system("unzip "+origin_file_path_prefix+str(file_len)+"/faq_"+str(file_len)+".zip -d "+destination_file_path_prefix+str(file_len))

        first_file_path_prefix = "./faq_"
        second_file_path_prefix = "/separate_faq_"

        file_path = first_file_path_prefix+str(file_len)+second_file_path_prefix+str(file_len)+"/Json.csv"
        file = open(file_path, 'w', encoding='utf-8')

        for i in range(file_len):
            file.write(str(i))
            if(i < file_len-1):
                file.write('\n')

        file.close()

        return file_len

if __name__ == "__main__":
    data_preprocessor = DataPreprocessor("./faq-test-file/faq2.5_hong.csv")
    data_preprocessor.processing()
