import json
import random

# 1. 字典初始化角色属性
role_data = {
    "name": "大狗嚼",
    "power": 10,
    "speed": 10,
    "agility": 10,
    "hp": 30000,  # 要求6：玩家血量30000
    "max_hp": 30000,
    "buffs": [],
    "skill_cooldown": 0  # 要求2：技能冷却计数器
}

# 初始化对手“哈基米”
enemy = {
    "name": "哈基米",
    "hp": 100000,  # 要求1：10万血量
    "max_hp": 100000,
    "base_attack": 1000,  # 基础伤害1000
    "current_attack": 1000,  # 当前伤害（每回合+200）
    "stun_turns": 0  # 眩晕回合数
}


# 2. 装饰器：暴击伤害翻倍
def crit_decorator(func):
    def wrapper(*args, **kwargs):
        damage = func(*args, **kwargs)
        # 要求2和1：玩家和对手都有30%概率暴击
        if random.random() < 0.3:
            print(f"[暴击触发] 最终伤害翻倍！")
            return int(damage * 2)
        return int(damage)

    return wrapper


# 3. 基础伤害计算
def calc_base_damage(power, speed, agility=1):
    """基础伤害 = power * speed * agility"""
    return power * speed * agility


# 4. 生成器：批量产出带数值的buff效果
def buff_generator():
    while True:  # 要求4：无限随机抽取
        buffs = [
            {"name": "力量1", "multiplier": 1.2},
            {"name": "力量2", "multiplier": 1.5},
            {"name": "力量3", "multiplier": 2.0}
        ]
        yield random.choice(buffs)


# 5. 列表推导式，生成合法加点范围 (0-20的偶数)
valid_points = [x for x in range(0, 21, 2)]

# 6. 通用属性加点函数（要求5：系统随机加点）
ALLOWED_ATTRS = ["power", "speed", "agility"]


def add_attribute():
    attr_name = random.choice(ALLOWED_ATTRS)
    value = random.choice(valid_points)
    role_data[attr_name] += value
    print(f"[系统加点] {attr_name} +{value}，当前值为 {role_data[attr_name]}")


# 7. 绑定装饰器的技能伤害函数
@crit_decorator
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


# 9. 主函数：回合制战斗菜单
def main():
    buff_gen = buff_generator()
    turn_count = 0

    print("=" * 30)
    print("   回合制对战：大狗嚼 VS 哈基米")
    print("=" * 30)

    while role_data["hp"] > 0 and enemy["hp"] > 0:
        turn_count += 1
        print(f"\n{'=' * 10} 第 {turn_count} 回合 {'=' * 10}")
        print(
            f"[玩家] HP: {role_data['hp']}/{role_data['max_hp']} | 属性: 力{role_data['power']} 速{role_data['speed']} 敏{role_data['agility']}")
        print(f"[哈基米] HP: {enemy['hp']}/{enemy['max_hp']} | 当前攻击力: {enemy['current_attack']}")

        # 玩家行动选择
        print("\n[1] 普通攻击 (力*速)")
        print("[2] 技能攻击 (力*速*敏，5回合CD)")
        print("[3] 盾反 (50%成功弹反并眩晕，失败受70%伤害)")
        print("[4] 使用Buff (消耗回合，持续2回合)")
        print("[5] 系统加点 (消耗回合)")
        print("[6] 恢复血量 (+1000 HP)")
        print("[7] 保存数据并退出")

        choice = input("请输入你的行动：").strip()

        player_action_done = False  # 标记玩家是否完成了消耗回合的行动

        # --- 玩家回合逻辑 ---
        if choice == "1":
            dmg = calc_base_damage(role_data["power"], role_data["speed"])
            # 应用buff
            for buff in role_data["buffs"]:
                dmg *= buff["multiplier"]

            # 暴击判定（通过装饰器）
            @crit_decorator
            def normal_attack():
                return dmg

            final_dmg = normal_attack()
            enemy["hp"] -= final_dmg
            print(f"你发动普通攻击，对哈基米造成 {final_dmg} 点伤害！")
            player_action_done = True

        elif choice == "2":
            if role_data["skill_cooldown"] > 0:
                print(f"技能冷却中！还需 {role_data['skill_cooldown']} 回合。")
                continue
            final_dmg = release_skill()
            enemy["hp"] -= final_dmg
            print(f"你释放技能，对哈基米造成 {final_dmg} 点伤害！")
            role_data["skill_cooldown"] = 5  # 要求2：5回合CD
            player_action_done = True

        elif choice == "3":
            print("你举起盾牌尝试盾反...")
            if random.random() < 0.5:  # 要求3：50%概率成功
                print(f"[盾反成功] 完美弹反了哈基米的攻击！哈基米陷入眩晕！")
                enemy["stun_turns"] = 1
            else:
                taken_dmg = int(enemy["current_attack"] * 0.7)  # 失败受70%伤害
                role_data["hp"] -= taken_dmg
                print(f"[盾反失败] 你受到了 {taken_dmg} 点伤害！")
            player_action_done = True

        elif choice == "4":
            new_buff = next(buff_gen)
            role_data["buffs"] = [new_buff]  # 要求4：同时只能持有一种buff
            print(f"获得新Buff: {new_buff['name']} (伤害倍率 x{new_buff['multiplier']})，持续2回合。")
            player_action_done = True

        elif choice == "5":
            add_attribute()
            player_action_done = True

        elif choice == "6":
            heal = 2000
            role_data["hp"] = min(role_data["hp"] + heal, role_data["max_hp"])
            print(f"你使用了恢复，回复了 {heal} 点生命值！")
            player_action_done = True

        elif choice == "7":
            save_role_data()
            print("游戏结束！")
            return

        else:
            print("无效选择，浪费了一回合！")
            player_action_done = True

        # 如果玩家执行了行动，处理回合结算
        if player_action_done:
            # 1. 检查敌人是否死亡
            if enemy["hp"] <= 0:
                print("\n🎉 恭喜你击败了哈基米！")
                break

            # 2. 处理Buff持续时间（要求4：持续2回合）
            if role_data["buffs"]:
                role_data["buffs"][0]["duration"] = role_data["buffs"][0].get("duration", 2) - 1
                if role_data["buffs"][0]["duration"] <= 0:
                    print(f"Buff [{role_data['buffs'][0]['name']}] 效果消失了。")
                    role_data["buffs"] = []

            # 3. 处理技能冷却
            if role_data["skill_cooldown"] > 0:
                role_data["skill_cooldown"] -= 1

            # 4. 哈基米的回合
            if enemy["stun_turns"] > 0:
                print(f"[哈基米] 处于眩晕状态，无法行动！")
                enemy["stun_turns"] -= 1
            else:
                # 哈基米攻击
                print(f"[哈基米] 发动攻击！")
                role_data["hp"] -= enemy["current_attack"]
                print(f"你受到了 {enemy['current_attack']} 点伤害！")

                # 哈基米每回合增加200攻击力（要求1）
                enemy["current_attack"] += 200

            # 5. 检查玩家是否死亡
            if role_data["hp"] <= 0:
                print("\n💀 你被哈基米击败了...")
                break


if __name__ == "__main__":
    main()