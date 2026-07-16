"""
main.py - 饮品店管理系统主程序
演示面向对象设计：抽象基类、继承、多态
"""
import sys
import os
# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from goods.coffee import Coffee
from goods.milk_cap import MilkCap
from goods.fruit_tea import FruitTea
from goods.base_drink import BaseDrink
from shop_tools import (
    check_positive,
    calc_total_price,
    save_order_with_with,
    read_all_orders,
    get_cheap_drinks,
    order_record_generator,
    sell_drink_thread_safe,
    multi_thread_sell,
    global_stock,
)


def demo_all_drinks():
    """演示所有饮品类"""
    print("=" * 50)
    print("   饮品店管理系统 - 全品类演示")
    print("=" * 50)

    # 创建各类饮品实例（多态：不同类型但都使用 BaseDrink 接口）
    coffee = Coffee("美式咖啡", 10)
    milk_cap = MilkCap("芝士葡萄", 15, milk_cap_cost=3.0)
    fruit_tea = FruitTea("杨枝甘露", 16)

    drinks = [coffee, milk_cap, fruit_tea]

    print("\n【饮品列表】")
    for drink in drinks:
        print(f"  {drink.name} - 单价: {drink.price}元, 库存: {drink.get_stock()}杯")

    # 演示多态：统一接口调用，各子类有不同实现
    print("\n【计算价格（多态演示）】")
    for drink in drinks:
        price = drink.get_final_price(2)
        print(f"  买2杯{drink.name}: {price}元")

    # 演示打印小票（多态，FruitTea 有额外输出）
    print("\n【打印小票】")
    for drink in drinks:
        drink.print_ticket(2)
        print()

    # 演示售卖
    print("【售卖饮品】")
    for drink in drinks:
        result = drink.sell(2)
        print(f"  {result}")


def demo_stock_management():
    """演示库存管理与多线程售卖"""
    print("\n" + "=" * 50)
    print("   库存管理与多线程售卖")
    print("=" * 50)

    print(f"\n当前库存: {global_stock}")
    print("\n启动多线程并发售卖...")
    multi_thread_sell()
    print(f"\n售卖后库存: {global_stock}")


def demo_tools():
    """演示 shop_tools 工具函数"""
    print("\n" + "=" * 50)
    print("   工具函数演示")
    print("=" * 50)

    # 1. 价格筛选
    drink_prices = {"珍珠奶茶": 12, "杨枝甘露": 16, "芝士葡萄": 15, "美式咖啡": 10}
    cheap = get_cheap_drinks(drink_prices, 14)
    print(f"\n价格 ≤14元的饮品: {cheap}")

    # 2. 总价计算
    total = calc_total_price(12, 3)
    print(f"珍珠奶茶 ×3 总价: {total}元")

    # 3. 生成器
    print("\n订单记录生成器:")
    orders = [("珍珠奶茶", 2, 24), ("杨枝甘露", 1, 16), ("芝士葡萄", 3, 42)]
    for record in order_record_generator(orders):
        print(f"  {record}")

    # 4. 正数检查
    print(f"\ncheck_positive(5): {check_positive(5)}")
    try:
        check_positive(-1)
    except ValueError as e:
        print(f"check_positive(-1): ValueError -> {e}")


def demo_discount():
    """演示全场折扣系统"""
    print("\n" + "=" * 50)
    print("   全场折扣系统演示")
    print("=" * 50)

    coffee = Coffee("美式咖啡", 10)
    milk_cap = MilkCap("芝士葡萄", 15)
    fruit_tea = FruitTea("杨枝甘露", 16)

    print(f"\n默认全场折扣: {BaseDrink.shop_discount}")
    print(f"  咖啡买2杯: {coffee.get_final_price(2)}元 (88折)")
    print(f"  奶盖茶买2杯: {milk_cap.get_final_price(2)}元 (立减3元)")
    print(f"  果茶买2杯: {fruit_tea.get_final_price(2)}元 (额外95折)")

    # 设置全场88折
    print(f"\n设置全场88折后:")
    BaseDrink.set_shop_discount(0.88)
    print(f"  咖啡买2杯: {coffee.get_final_price(2)}元 (88折 × 88折)")
    print(f"  奶盖茶买2杯: {milk_cap.get_final_price(2)}元 (88折后立减3元)")
    print(f"  果茶买2杯: {fruit_tea.get_final_price(2)}元 (88折 × 95折)")

    BaseDrink.set_shop_discount(1.0)  # 恢复默认


def main():
    """主函数"""
    demo_all_drinks()
    demo_discount()
    demo_tools()
    demo_stock_management()

    print("\n" + "=" * 50)
    print("   所有演示完成，系统运行正常！")
    print("=" * 50)


if __name__ == "__main__":
    main()
