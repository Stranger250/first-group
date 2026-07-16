# goods/fruit_tea.py - 果茶子类
# 继承BaseDrink，实现果茶专属优惠：全场折扣基础上额外95折
import sys
import os
# 添加项目根目录到路径，使直接运行此文件时能找到 shop_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from goods.base_drink import BaseDrink


class FruitTea(BaseDrink):
    """
    果茶类
    专属优惠：全场折扣基础上额外95折
    """

    def __init__(self, name: str, price: float):
        """
        初始化果茶
        :param name: 名称
        :param price: 单价
        """
        super().__init__(name, price)

    def get_final_price(self, buy_num: int) -> float:
        """
        计算果茶的最终价格
        专属优惠：全场折扣基础上额外95折
        :param buy_num: 购买数量
        :return: 最终价格
        """
        origin = self.price * buy_num
        final = origin * self.shop_discount * 0.95
        return round(final, 2)

    def print_ticket(self, buy_num: int):
        """
        打印订单票，显示果茶专属优惠信息
        :param buy_num: 购买数量
        """
        total = self.get_final_price(buy_num)
        origin = self.price * buy_num
        print(f"饮品：{self.name}, 数量：{buy_num}, 总价：{total}")
        print(f"（果茶专属优惠：额外95折，原价：{origin}，全场折扣：{self.shop_discount}，最终价：{total}）")


# 测试代码
if __name__ == "__main__":
    print("===== fruit_tea.py 模块自测 =====\n")

    # 1. 创建果茶实例
    fruit_tea = FruitTea("杨枝甘露", 16)
    print(f"饮品：{fruit_tea.name}，单价：{fruit_tea.price}")
    print(f"当前库存：{fruit_tea.get_stock()}")

    # 2. 测试计算最终价格
    print(f"\n买1杯总价：{fruit_tea.get_final_price(1)}（全场折扣={BaseDrink.shop_discount}，额外95折）")
    print(f"买2杯总价：{fruit_tea.get_final_price(2)}")

    # 3. 测试打印小票（含果茶专属优惠信息）
    print()
    fruit_tea.print_ticket(2)

    # 4. 测试全场折扣叠加效果
    print(f"\n设置全场88折后：")
    BaseDrink.set_shop_discount(0.88)
    fruit_tea.print_ticket(2)
    BaseDrink.set_shop_discount(1.0)  # 恢复默认

    # 5. 测试售卖
    print(f"\n售卖前库存：{fruit_tea.get_stock()}")
    result = fruit_tea.sell(3)
    print(result)

    print("\n===== 测试完成 =====")
