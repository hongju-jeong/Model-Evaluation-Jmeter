import json
class Comparator():
    def __init__(self, file_num_list):
        self.file_num_list = file_num_list

    def sort_response_data(self):
        test_faq_prefix = "./test_faq_"

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

    def run(self):
        self.sort_response_data()



        

if __name__ == "__main__":
    file_num_list = [100,500,660]
    comparator = Comparator(file_num_list)
    comparator.run()
