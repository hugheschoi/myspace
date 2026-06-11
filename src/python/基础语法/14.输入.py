def get_valid_input(prompt, input_type=str, validation_func=None):
    """
    获取有效的用户输入

    参数:
        prompt: 提示信息
        input_type: 期望的数据类型
        validation_func: 自定义验证函数
    """
    while True:
        try:
            user_input = input(prompt)

            # 类型转换
            if input_type != str:
                user_input = input_type(user_input)

            # 自定义验证
            if validation_func and not validation_func(user_input):
                print("输入不符合要求，请重新输入。")
                continue

            return user_input

        except ValueError:
            print(f"错误：请输入有效的{input_type.__name__}类型数据！")
        except Exception as e:
            print(f"发生错误：{e}")


# 使用示例
age = get_valid_input("请输入年龄：", int, lambda x: 0 <= x <= 150)
print(f"你的年龄：{age}")

email = get_valid_input("请输入邮箱：", str, lambda x: "@" in x)
print(f"你的邮箱：{email}")
