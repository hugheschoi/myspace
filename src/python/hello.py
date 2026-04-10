num = 42

# 方法1：使用字符串切片
hex_with_prefix = hex(num)  # 0x2a
hex_without_prefix_1 = hex_with_prefix[2:]  # 从第2个字符开始截取 2a
print(hex_without_prefix_1)  # 2a

# 方法2：使用格式化字符串 (f-string) - 更推荐！
# 格式： `：x` 表示十六进制， `：b` 表示二进制， `：o` 表示八进制
hex_without_prefix_2 = f"{num:x}"  # 小写
hex_without_prefix_3 = f"{num:X}"  # 大写
bin_without_prefix = f"{num:b}"

print(hex_without_prefix_2)  # 输出： 2a
print(hex_without_prefix_3)  # 输出： 2A
print(bin_without_prefix)  # 输出： 101010
