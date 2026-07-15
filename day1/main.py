import json

# 1. 字典初始化角色属性（新增三维属性与buff列表）
role_data = {
    "name": "大狗嚼",
    "power": 10,
    "speed": 10,
    "agility": 10,
    "buffs": []
}


# 2. 装饰器：双倍伤害的挂件
def double_damage(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"[暴击触发] 最终伤害翻倍！")
        return result * 2

    return wrapper


# 3. 基础伤害计算（替换lambda，使用新公式）
def calc_base_damage(power, speed, agility):
    """基础伤害 = power * speed * agility"""
    return power * speed * agility


# 4. 生成器：批量产出带数值的buff效果
def buff_generator():
    buffs = [
        {"name": "力量1", "multiplier": 1.2},  # 伤害提升20%
        {"name": "力量2", "multiplier": 1.5},  # 伤害提升50%
        {"name": "力量3", "multiplier": 2.0}  # 伤害提升100%
    ]
    for buff in buffs:
        yield buff


# 5. 列表推导式，生成合法加点范围 (0-20的偶数)
valid_points = [x for x in range(0, 21, 2)]

# 6. 通用属性加点函数（支持三种属性）
ALLOWED_ATTRS = ["power", "speed", "agility"]


def add_attribute(attr_name, value):
    if attr_name not in ALLOWED_ATTRS:
        print(f"加点失败：不支持的属性 '{attr_name}'，仅支持 {ALLOWED_ATTRS}")
        return
    if value not in valid_points:
        print(f"加点失败：{value} 不是合法数值（必须是0-20的偶数）")
        return

    role_data[attr_name] += value
    print(f"加点成功：{attr_name} +{value}，当前值为 {role_data[attr_name]}")


# 7. 绑定装饰器的技能伤害函数（融入Buff计算）
@double_damage
def release_skill():
    base_dmg = calc_base_damage(
        role_data["power"],
        role_data["speed"],
        role_data["agility"]
    )
    buff_multiplier = 1.0
    active_buff_names = []
    for buff in role_data["buffs"]:
        buff_multiplier *= buff["multiplier"]
        active_buff_names.append(buff["name"])

    final_before_crit = base_dmg * buff_multiplier

    print(f"基础伤害: {base_dmg}")
    if active_buff_names:
        print(f"生效Buff: {', '.join(active_buff_names)} (总倍率: {buff_multiplier})")
        print(f"Buff加成后伤害: {final_before_crit}")

    return final_before_crit


# 8. with实现角色数据存档
def save_role_data():
    with open('role_save.json', "w", encoding="utf-8") as f:
        json.dump(role_data, f, ensure_ascii=False, indent=4)
    print("角色数据已成功存档至 role_save.json")


# 9. 主函数：交互菜单
def main():
    buff_gen = buff_generator()

    print("=" * 30)
    print("   欢迎来到 Python 角色系统")
    print("=" * 30)

    while True:
        print("\n[1] 查看角色面板")
        print("[2] 属性加点 (power/speed/agility)")
        print("[3] 获取Buff")
        print("[4] 释放技能")
        print("[5] 保存数据")
        print("[0] 退出游戏")

        choice = input("请输入选择：").strip()

        if choice == "1":
            print("\n--- 角色面板 ---")
            for k, v in role_data.items():
                print(f"  {k}: {v}")

        elif choice == "2":
            attr = input("输入属性名 (power/speed/agility): ").strip()
            try:
                val = int(input("输入加点数值 (0-20偶数): "))
                add_attribute(attr, val)
            except ValueError:
                print("请输入纯数字！")

        elif choice == "3":
            try:
                new_buff = next(buff_gen)
                role_data["buffs"].append(new_buff)
                print(f"获得新Buff: {new_buff['name']} (伤害倍率 x{new_buff['multiplier']})")
            except StopIteration:
                print("已获取全部Buff！")

        elif choice == "4":
            final = release_skill()
            print(f"最终结算伤害: {final}\n")

        elif choice == "5":
            save_role_data()

        elif choice == "0":
            print("再见！")
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    main()