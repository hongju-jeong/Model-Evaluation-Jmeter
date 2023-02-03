import pandas as pd
import os
import random

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
        if(len(df_faq)<1000):
            last_file_number = file_num_list.pop()

        for file_number in file_num_list:
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
            df_output_question.to_csv(file_name, index=False, encoding='utf-8-sig')
            

    def run(self):
        file_len = self.check_amount_of_items_origin_file()
        print(file_len)
        file_num_list = self.make_separate_faq_dir(file_len)
        self.random_extract_data(file_num_list)





if __name__ == "__main__":
    data_preprocessor = DataPreprocessor("./faq-test-file/faq2.5_hong.csv")
    data_preprocessor.run()
