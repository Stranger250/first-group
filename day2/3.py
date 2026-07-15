import time

class AIModel:
    def __init__(self, name, model_type):
        self.name = name
        self.model_type = model_type

    def predict(self, input_data):
        print(f"{self.name}模型收到输入：{input_data}，但具体推理逻辑由子类实现")
        return "父类默认结果"

class TextModel(AIModel):
    def predict(self, input_data):
        time.sleep(1)
        print(f"文本模型{self.name}正在生成文本...")
        return f"生成的文本结果: {input_data}"


class ImageModel(AIModel):
    def predict(self, input_data):
        time.sleep(2)
        print(f"图像模型{self.name}正在识别图像...")
        return f"识别结果: {input_data}"


if __name__ == "__main__":
    text_model = TextModel("文心一言", "NLP")
    text_result = text_model.predict("今天天气真好")
    print(text_result)
    image_model = ImageModel("通义万相", "CV")
    image_result = image_model.predict("一张猫的图片")
    print(image_result)
