class WorkingDog:
    energy=100
    def __init__(self, name, species,job):
        self.name = name
        self.species = species
        self.job = job

    def work(self):
        self.energy=self.energy-40
        if self.energy >= 40:
            print(f"{self.name}执行了{self.job}任务，剩余精力{self.energy}")
        else:
            print(f"{self.name}精力不足，无法执行任务")

    def play(self):
        self.energy=self.energy-20
        if self.energy >= 0:
            print(f"{self.name}虽然是工作犬，但也要放松一下，剩余精力{self.energy}")
        else:
            print(f"{self.name}累坏了，玩不动了")

    def eat(self):
        self.energy=self.energy+30
        if self.energy <= 100:
            print(f"{self.name}吃饱了，精力恢复到{self.energy}")
        elif 200 >= self.energy > 100:
            print(f"{self.name}吃撑了，别喂了")
        elif 230 >= self.energy > 200:
            print(f"别喂{self.name}了，再喂要撑死了")
        else:
            print(f"{self.name}死了")

dahuang = WorkingDog("大黄", "狗","导盲")

dahuang.work()
dahuang.work()
dahuang.play()
dahuang.play()
dahuang.eat()

