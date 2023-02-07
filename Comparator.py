import json
import re
import pandas as pd
import os

class Comparator():
    def __init__(self, file_num_list):
        self.file_num_list = file_num_list

    def sort_response_data(self):
        test_faq_prefix = "./test_faq_"

        for file_num in self.file_num_list:
            origin_file = open(test_faq_prefix+str(file_num)+"/faq"+str(file_num)+".json",'r',encoding='utf-8')
            lines = origin_file.readlines()
            origin_file.close()

            wf = open(test_faq_prefix+str(file_num)+"/faq"+str(file_num)+".json",'w',encoding='utf-8')
            for i in range(len(lines)):
                if(i == 0):
                    wf.write('[')
                    wf.write(lines[i])
                elif(i == (len(lines)-1)):
                    wf.write(lines[i][:-2])
                    wf.write(']')
                else : wf.write(lines[i])
            
            wf.close()


        for file_num in self.file_num_list:
            json_file = open(test_faq_prefix+str(file_num)+"/faq"+str(file_num)+".json",'r',encoding='utf-8')
            json_data = json.load(json_file)
            json_file.close()

            with open(test_faq_prefix+str(file_num)+"/faq"+str(file_num)+".json",'w',encoding='utf-8') as make_file:
                make_file.write('[')
                for i in range(len(json_data)):
                    json_data[i]['recipient_id'] = int(json_data[i]['recipient_id'])
                    json.dump(json_data[i], make_file, ensure_ascii=False)
                    if(i < len(json_data)-1):
                        make_file.write(',\n')
                make_file.write(']')
            
            json_file = open(test_faq_prefix+str(file_num)+"/faq"+str(file_num)+".json",'r',encoding='utf-8')
            json_data = json.load(json_file)
            json_file.close()

            sorted_json_data = sorted(json_data, key=(lambda x: x['recipient_id']))

            with open(test_faq_prefix+str(file_num)+"/faq"+str(file_num)+".json",'w',encoding='utf-8') as make_file:
                make_file.write('[')
                for i in range(len(sorted_json_data)):
                    sorted_json_data[i]['recipient_id'] = str(sorted_json_data[i]['recipient_id'])
                    json.dump(sorted_json_data[i], make_file, ensure_ascii=False)
                    if(i < len(sorted_json_data)-1):
                        make_file.write(',\n')
                make_file.write(']')

    def mkdir_for_result(self):
        os.mkdir('result')

    def make_compare_result(self):
        json_prefix = "./test_faq_"
        csv_prefix = "./separate_faq_"

        hangul = re.compile('[^ㄱ-ㅣ가-힣]+')

        for file_num in self.file_num_list:
            json_file = open(json_prefix+str(file_num)+"/faq"+str(file_num)+".json","r", encoding="utf-8")
            json_data = json.load(json_file)
            json_file.close()

            df = pd.read_csv(csv_prefix+str(file_num)+"/faq_"+str(file_num)+".csv", sep=',', encoding='utf-8')
            df_output = pd.DataFrame(columns=("recipient_id","question","answer","response","intent"))
            
            count = 0
            for i in range(len(df)):
                recipient_id = json_data[i]['recipient_id']
                question = str(df.iat[i,0])
                answer = str(df.iat[i,1])
                response = json_data[i]['text']
                intent = json_data[i]['intent']
                answer_han = hangul.sub('', answer)
                response_han = hangul.sub('', response)
                if(answer_han != response_han):
                    df_output.loc[i] = [recipient_id, question, answer, response, intent]
                    count +=1

            df_output = df_output.reset_index(drop=True)
            df_output.loc[0, "질문 개수"] = file_num      # index를 없애던가 맨 위를 가리키도록 바꾸기
            df_output.loc[0, "정답 횟수"] = file_num - count
            df_output.loc[0, "정답 비율(%)"] = ((file_num - count)/file_num)*100


            file_name = "./result/result_faq_"+str(file_num)+".csv"
            df_output.to_csv(file_name, index=False, encoding='utf-8-sig')


    def run(self):
        self.sort_response_data()
        self.mkdir_for_result()
        self.make_compare_result()



        

if __name__ == "__main__":
    file_num_list = [100,500,660]
    comparator = Comparator(file_num_list)
    comparator.run()
