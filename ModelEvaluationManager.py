import os

class ModelEvaluationManager():
    def __init__(self):
        self.origin_file_path = ""

    def fine_origin_file(self):
        file_list = os.listdir("./faq-test-file")
        self.origin_file_path = "./faq-test-file/"+file_list[0]

    def run(self):
        self.fine_origin_file()
        



if __name__ == "__main__":
    model_evaluation_manager = ModelEvaluationManager()
    model_evaluation_manager.run()