import time
from datetime import datetime
import threading

lock = threading.Lock() #锁

class AIModel():#模型基类，有抽象方法predict
    def __init__(self,name,model_type):
        self.name = name
        self.model_type = model_type
    
    def predict(self,input_data):
        print(f"{self.name}模型收到输入：{input_data}，但具体推理逻辑由子类实现")
        raise NotImplementedError("子类必须实现predict方法")
    
class TextModel(AIModel):#文本模型，继承AIModel类，实现predict方法
    def __init__(self,name,model_type):
        super().__init__(name,model_type)

    def predict(self,input_data):
        print(f"文本模型{self.name}正在生成文本...")
        time.sleep(1)
        return f"生成的文本结果：{input_data}"

class ImageModel(AIModel):#图像模型，继承AIModel类，实现predict方法
    def __init__(self,name,model_type):
        super().__init__(name,model_type)

    def predict(self,input_data):
        print(f"图像模型{self.name}正在识别图像...")
        time.sleep(2)
        return f"识别结果：{input_data}"
    
class AudioModel(AIModel):#音频模型，继承AIModel类，实现predict方法
    def __init__(self,name,model_type):
        super().__init__(name,model_type)

    def predict(self,input_data):
        print(f"音频模型{self.name}正在接受并处理音频...")
        time.sleep(3)
        return f"处理结果：{input_data}"
    
class Scheduler() :#调度器类
    records = []  #任务记录列表
    def __init__(self,lock):
        self.lock = lock
    
    def _run_one(self,model,data):  # 运行一个任务
        task_dict = {}
        start = datetime.now()
        result = model.predict(data)
        print(f"{model.name}完成运行，结果为：{result}")
        end = datetime.now()
        cost = int(end.timestamp() - start.timestamp())
        print(f"任务耗时: {cost}秒")
        task_dict['model名'] = model.name
        task_dict['start'] = start.strftime('%Y年%m月%d日 %H点%M分%S秒')
        task_dict['end'] = end.strftime('%Y年%m月%d日 %H点%M分%S秒')
        task_dict['cost'] = cost
        task_dict['result'] = result  #将所有数据处理为字典
        self.lock.acquire()
        self.records.append(task_dict)   #上锁并添加任务记录
        self.lock.release()
    
    def run_serial(self,model_list,input_data):  # 串行运行任务
        print(f"模型数量: {len(model_list)}, 数据数量: {len(input_data)}")
        start = datetime.now().timestamp()
        for i in range(0,len(model_list)):
            self._run_one(model_list[i],input_data[i])
        end = datetime.now().timestamp()
        print(f"总耗时: {int(end-start)}秒")
    
    def run_concurrent(self,model_list,input_data):  # 并发运行任务
        threads = []
        start = datetime.now().timestamp()
        for i in range(0,len(model_list)):  #创建线程
            tl = threading.Thread(target=self._run_one, args=(model_list[i],input_data[i]))
            tl.start()
            threads.append(tl)
        for i in threads:  #等待所有线程完成
            i.join()
        end = datetime.now().timestamp()
        print(f"总耗时: {int(end-start)}秒")

    def report(self):   #生成报告
        with open('report.txt', 'w') as f:
            for i in self.records:
                print(i)
                f.write(str(i) + '\n')

model_list = []
input_data = []

for i in range(6):  #创建模型
    model_type = int(input('请输入模型种类(0为文本模型，1为图像模型，2为音频模型)：'))
    model_name = input('请输入模型名称：')
    match model_type:
        case 0:
            model = TextModel(model_name, model_type)
            model_list.append(model)
        case 1:
            model = ImageModel(model_name, model_type)
            model_list.append(model)
        case 2:
            model = AudioModel(model_name, model_type)
            model_list.append(model)
        case _:
            print('输入错误！请重新输入！')


scheduler1 = Scheduler(lock) #创建调度器
while True:
    choose = int(input("请选择运行模式(0执行单任务，1串行执行任务，2并发执行任务，3输出并打印报告，4退出)):"))
    match choose:
        case 0: #单任务
            num = len(model_list)
            choose_model = int(input(f"请选择要执行的模型序号(你现在有{num}个模型,1-{num})：")) - 1
            data = input("请输入输入数据：")
            scheduler1._run_one(model_list[choose_model],data)
        case 1: #串行执行任务
            for i in range(len(model_list)):
                data = input(f"请输入第{i+1}个模型的输入数据：")
                input_data.append(data)
            scheduler1.run_serial(model_list,input_data)
        case 2: #并发执行任务
            for i in range(len(model_list)):
                data = input(f"请输入第{i+1}个模型的输入数据：")
                input_data.append(data)
            scheduler1.run_concurrent(model_list,input_data)
        case 3: #输出并打印报告
            scheduler1.report()
        case 4: #退出
            print("已退出")
            break

