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
        df_faq = pd.read_csv(self.origin_file_path, sep = ',', encoding='utf-8')
        return len(df_faq)

    def make_separate_faq_dir(self, file_len):
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

        file_path_prefix = "./faq_"
        for file_num in file_num_list:
            os.mkdir(file_path_prefix+str(file_num))

    def unzip_faq_data(self, file_num_list):
        origin_file_path_prefix = "./separate_faq_"
        destination_file_path_prefix = "./faq_"

        for file_num in file_num_list:
            os.system("unzip "+origin_file_path_prefix+str(file_num)+"/faq_"+str(file_num)+".zip -d "+destination_file_path_prefix+str(file_num))

    def make_csv_for_index(self, file_num_list):
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
        file_len = self.check_amount_of_items_origin_file()
        print(file_len)
        file_num_list = self.make_separate_faq_dir(file_len)
        self.random_extract_data(file_num_list)
        self.separate_to_json(file_num_list)
        self.mkdir_for_test(file_num_list)
        self.unzip_faq_data(file_num_list)
        self.make_csv_for_index(file_num_list)


        return file_num_list





if __name__ == "__main__":
    data_preprocessor = DataPreprocessor("./faq-test-file/faq2.5_hong.csv")
    data_preprocessor.processing()
