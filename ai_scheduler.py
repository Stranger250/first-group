import time
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


#   模型层
class AIModel:
    def __init__(self, name, model_type):
        self.name = name
        self.model_type = model_type

    def predict(self, input_data):
        raise NotImplementedError("子类必须实现 predict 方法")

class TextModel(AIModel):
    def predict(self, input_data):
        start = time.time()
        time.sleep(1)
        cost =round(time.time() - start,2)
        result = f"生成的文本结果: {input_data}"
        return result, cost

class ImageModel(AIModel):
    def predict(self, input_data):
        start = time.time()
        time.sleep(2)
        cost = time.time() - start
        result = f"图像识别结果: {input_data}"
        return result, cost

class AudioModel(AIModel):
    def predict(self, input_data):
        start = time.time()
        time.sleep(1.5)
        cost = round(time.time() - start, 2)
        result = f"语音识别结果: {input_data}"
        return result, cost


#   调度器 Scheduler
class Scheduler:

    #初始化调度器，创建任务记录表、线程锁和任务队列。
    def __init__(self):
        self.records = []
        self.lock = threading.Lock()
        self.tasks = []

    # 向调度器添加一个待执行任务。
    def add_task(self, user_name, model, input_data):
        self.tasks.append((user_name, model, input_data))

    #单任务
    def _run_one(self, user_name, model, input_data):
        result, cost = model.predict(input_data)
        record = {
            "user": user_name,
            "model": model.name,
            "cost": cost,
            "result": result
        }
        with self.lock:
            self.records.append(record)

    #串行
    def run_serial(self):
        for task in self.tasks:
            self._run_one(*task)

    #并行
    def run_concurrent(self):
        threads = []
        for task in self.tasks:
            t = threading.Thread(target=self._run_one, args=task)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

    #加了ThreadPoolExecutor的并行
    def run_concurrent_pool(self, max_workers=4):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self._run_one, *task) for task in self.tasks]
            for future in futures:
                future.result()

    # 打印
    def report(self):
        print("\n===== 任务执行详情 =====")
        for i, record in enumerate(self.records, 1):
            print(f"任务 {i}: 用户[{record['user']}] | 模型[{record['model']}] | "
                  f"耗时[{record['cost']}秒] | 结果[{record['result']}]")

#   主程序 main
def main():

    # 创建模型
    text_model = TextModel("deepseek", "NLP")
    image_model = ImageModel("seedance", "CV")
    audio_model = AudioModel("whisper", "Audio")

    # 构造调度器并添加混合用户任务
    scheduler = Scheduler()
    scheduler.add_task("User1", text_model, "你好，世界")
    scheduler.add_task("User2", text_model, "Python没意思")
    scheduler.add_task("User3", image_model, "一张的基米图片")
    scheduler.add_task("User4", image_model, "一张大狗的图片")
    scheduler.add_task("User5", text_model, "今天天气不错")
    scheduler.add_task("User6", image_model, "一张汽车人的图片")
    scheduler.add_task("User7", audio_model, "一段会议录音")
    scheduler.add_task("User8", audio_model, "一首周杰伦的歌")

    # 运行串行并统计全局总耗时
    start_serial = time.time()
    scheduler.run_serial()
    cost_serial = round(time.time() - start_serial, 2)

    # 清空记录，准备并发测试
    scheduler.records.clear()

    # 运行线程池并发，统计全局总耗时
    start_concurrent = time.time()
    scheduler.run_concurrent_pool(max_workers=4)
    cost_concurrent = round(time.time() - start_concurrent, 2)

    # 生成对比报表数据
    saved_time = round(cost_serial - cost_concurrent, 2)
    speed_up = round(cost_serial / cost_concurrent, 2) if cost_concurrent > 0 else 0
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_lines = [
        "\n" + "=" * 40,
        "性能对比报表",
        "=" * 40,
        f"串行总耗时:{cost_serial} 秒",
        f"并发总耗时:{cost_concurrent} 秒",
        f"节省时长:{saved_time} 秒",
        f"加速比:{speed_up} 倍",
        f"当前时间:{current_time}",
        "=" * 40
    ]
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    # 输出
    for line in report_lines:
        print(line)


if __name__ == "__main__":
    main()


