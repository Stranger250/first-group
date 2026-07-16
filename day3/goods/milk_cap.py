# goods/milk_cap.py - 奶盖茶子类
# 继承BaseDrink，实现奶盖茶专属优惠：购买2杯及以上立减3元
import sys
import os
# 添加项目根目录到路径，使直接运行此文件时能找到 shop_tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from goods.base_drink import BaseDrink


class MilkCap(BaseDrink):
    """
    奶盖茶类
    专属优惠：购买2杯及以上立减3元
    """

    def __init__(self, name: str, price: float, milk_cap_cost: float = 3.0):
        """
        初始化奶盖茶
        :param name: 名称
        :param price: 单价
        :param milk_cap_cost: 奶盖单杯价格
        """
        super().__init__(name, price)
        # 私有属性：奶盖单杯价格
        self.__milk_cap_cost = milk_cap_cost

    def get_milk_cap_cost(self) -> float:
        """获取奶盖的单杯价格"""
        return self.__milk_cap_cost

    def get_final_price(self, buy_num: int) -> float:
        """
        计算奶盖茶的最终价格
        专属优惠：购买2杯及以上立减3元
        :param buy_num: 购买数量
        :return: 最终价格
        """
        origin = self.price * buy_num
        final = origin * self.shop_discount
        if buy_num >= 2:
            final -= 3
        return round(final, 2)


# 测试代码
if __name__ == "__main__":
    print("===== milk_cap.py 模块自测 =====\n")

    # 1. 创建奶盖茶实例
    milk_cap = MilkCap("芝士葡萄", 15, milk_cap_cost=3.0)
    print(f"饮品：{milk_cap.name}，单价：{milk_cap.price}")
    print(f"奶盖单杯价格：{milk_cap.get_milk_cap_cost()}")

    # 2. 测试购买1杯（不触发优惠）
    print(f"\n买1杯总价：{milk_cap.get_final_price(1)}（无优惠）")

    # 3. 测试购买2杯（触发立减3元）
    print(f"买2杯总价：{milk_cap.get_final_price(2)}（立减3元）")

    # 4. 测试购买3杯（触发立减3元）
    print(f"买3杯总价：{milk_cap.get_final_price(3)}（立减3元）")

    # 5. 测试打印小票
    print()
    milk_cap.print_ticket(2)

    # 6. 测试类方法：全场折扣
    print(f"\n设置全场88折前，买2杯：{milk_cap.get_final_price(2)}")
    BaseDrink.set_shop_discount(0.88)
    print(f"设置全场88折后，买2杯：{milk_cap.get_final_price(2)}")
    BaseDrink.set_shop_discount(1.0)  # 恢复默认

    print("\n===== 测试完成 =====")
