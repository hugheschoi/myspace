# binary: 二进制 缩写 bin 逢二进一
# 十六进制缩写 hex, 十六进制是逢十六进一，使用0-9和a-f表示0-15
# 八进制缩写 oct， 八进制是逢八进一，使用0-7表示0-7

# 字面量
dec_num = 42  # 十进制
hex_num = 0x2A  # 十六进制，0x开头
oct_num = 0o52  # 八进制，0o开头
bin_num = 0b101010  # 二进制，0b开头
print(bin_num)  # 输出： 42 会以十进制显示

# 转换函数
# bin(i) -> 二进制字符串
# oct(i) -> 八进制字符串
# hex(i) -> 十六进制字符串
num = 42
print(bin(num))  # 输出： 0b101010
print(hex(num))  # 输出： 0x2a
print(oct(num))  # 输出： 0o52

# 将字符串转换为十进制整数
# int(s, base) -> 将字符串s按照base进制转换为十进制整数
bin_str = "101010"
oct_str = "52"
hex_str = "2a"
print(int(bin_str, 2))  # 输出： 42
print(int(oct_str, 8))  # 输出： 42
print(int(hex_str, 16))  # 输出： 42

# 处理颜色值
# RGB颜色通常表示为十六进制字符串，例如 #RRGGBB
color_hex = "#FF5733"
# 提取RGB分量
r = int(color_hex[1:3], 16)  # 红色分量
g = int(color_hex[3:5], 16)  # 绿色分量
b = int(color_hex[5:7], 16)  # 蓝色分量
print(f"RGB: ({r}, {g}, {b})")  # 输出： RGB: (255, 87, 51)

# 格式化输出（去掉前缀）
# [2:] 表示从字符串的第2个字符开始截取，去掉前缀0b、0o、0x
print(f"Hex: {hex(num)[2:]}")  # 输出： Hex: 2a
print(f"Binary: {bin(num)[2:]}")  # 输出： Binary: 101010
print(f"Octal: {oct(num)[2:]}")  # 输出： Octal: 52
