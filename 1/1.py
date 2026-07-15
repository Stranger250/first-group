import time
import threading
from datetime import datetime


class AIModel:
    """
    AI模型父类，抽象基类，定义通用属性与predict抽象接口
    """
    def __init__(self, name, model_type):
        """
        初始化AI基础模型
        :param name: 模型名称
        :param model_type: 模型类型（文本/图像）
        """
        self.name = name
        self.model_type = model_type

    def predict(self, input_data):
        """
        推理抽象方法，子类必须重写实现
        :param input_data: 用户输入数据
        :return: 推理结果字典，包含输出文本与耗时
        """
        raise NotImplementedError("子类必须重写predict推理方法")


class TextModel(AIModel):
    """
    文本生成模型，继承AIModel父类
    """
    def predict(self, input_data):
        """
        文本推理，模拟1秒推理耗时
        :param input_data: 用户文本指令
        :return: dict 推理输出、耗时秒数
        """
        task_start = datetime.now()
        print(f"[{self.name}] 文本推理开始，输入：{input_data}")
        time.sleep(1)
        task_end = datetime.now()
        cost = (task_end - task_start).total_seconds()
        output = f"文本生成结果：《{input_data}》创作完成"
        return {"output": output, "cost": cost}


class ImageModel(AIModel):
    """
    图像识别模型，继承AIModel父类
    """
    def predict(self, input_data):
        """
        图像推理，模拟2秒推理耗时
        :param input_data: 图片文件路径
        :return: dict 识别输出、耗时秒数
        """
        task_start = datetime.now()
        print(f"[{self.name}] 图像识别开始，图片：{input_data}")
        time.sleep(2)
        task_end = datetime.now()
        cost = (task_end - task_start).total_seconds()
        output = f"图像识别结果：{input_data} 检测到目标物体"
        return {"output": output, "cost": cost}


class Scheduler:
    """
    任务调度指挥官：统一管理串行、并发任务，记录任务日志，输出报表
    """
    def __init__(self):
        """初始化调度器：任务记录表、线程互斥锁"""
        self.records = []
        self.lock = threading.Lock()

    def _run_one(self, user_name, model, input_data):
        """
        内部私有方法：执行单个用户任务，加锁写入记录
        :param user_name: 请求用户名
        :param model: AIModel子类实例
        :param input_data: 用户输入数据
        """
        res_dict = model.predict(input_data)
        record = {
            "user": user_name,
            "model_name": model.name,
            "model_type": model.model_type,
            "input": input_data,
            "output": res_dict["output"],
            "task_cost": round(res_dict["cost"], 2)
        }
        # 加锁保护共享列表写入
        with self.lock:
            self.records.append(record)

    def run_serial(self, task_list):
        """
        串行执行所有任务：排队依次运行
        :param task_list: 任务列表，每个元素元组 (用户名,模型实例,输入数据)
        :return: float 本轮串行总耗时
        """
        self.records.clear()
        start = datetime.now()
        for task in task_list:
            self._run_one(*task)
        end = datetime.now()
        total_cost = (end - start).total_seconds()
        return round(total_cost, 2)

    def run_concurrent(self, task_list):
        """
        多线程并发执行所有任务，全部启动后等待完成
        :param task_list: 任务列表，每个元素元组 (用户名,模型实例,输入数据)
        :return: float 本轮并发总耗时
        """
        self.records.clear()
        start = datetime.now()
        thread_pool = []
        for task in task_list:
            t = threading.Thread(target=self._run_one, args=task)
            thread_pool.append(t)
        # 统一启动所有线程
        for t in thread_pool:
            t.start()
        # 阻塞等待全部线程结束
        for t in thread_pool:
            t.join()
        end = datetime.now()
        total_cost = (end - start).total_seconds()
        return round(total_cost, 2)

    def report(self, run_mode):
        """
        格式化打印当前所有任务明细日志
        :param run_mode: 运行模式标识：串行/并发
        """
        print(f"\n==================== {run_mode} 任务明细 ====================")
        for idx, item in enumerate(self.records, 1):
            print(f"任务{idx} | 用户：{item['user']} | 模型：{item['model_name']}({item['model_type']})")
            print(f"    输入指令：{item['input']}")
            print(f"    推理输出：{item['output']}")
            print(f"    单任务耗时：{item['task_cost']} 秒\n")


def main():
    """
    主程序入口：创建模型、构造6条混合任务、分别跑串行与并发、输出对比报表
    """
    # 1. 初始化两种AI模型
    text_llm = TextModel("文智大模型", "文本生成")
    image_det = ImageModel("图像检测器", "图像识别")

    # 2. 构造6条混合用户任务（文本+图像穿插）
    all_tasks = [
        ("用户A", text_llm, "写一篇春天散文"),
        ("用户B", image_det, "street.jpg"),
        ("用户C", text_llm, "生成Python排序代码"),
        ("用户D", image_det, "animal.png"),
        ("用户E", text_llm, "讲一个科幻小故事"),
        ("用户F", image_det, "food.jpg")
    ]

    # 3. 创建调度指挥官实例
    commander = Scheduler()

    # 串行执行并计时
    serial_total = commander.run_serial(all_tasks)
    commander.report("【串行模式】")

    # 并发执行并计时
    concurrent_total = commander.run_concurrent(all_tasks)
    commander.report("【多线程并发模式】")

    # 4. 生成完整性能对比报表
    save_time = serial_total - concurrent_total
    speed_up = round(serial_total / concurrent_total, 2)
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("==================== 全局性能对比报表 ====================")
    print(f"当前系统时间：{now_time}")
    print(f"串行全部任务总耗时：{serial_total} 秒")
    print(f"多线程并发总耗时：{concurrent_total} 秒")
    print(f"并发节省时长：{save_time:.2f} 秒")
    print(f"并发加速比：{speed_up} 倍")


if __name__ == "__main__":
    main()
