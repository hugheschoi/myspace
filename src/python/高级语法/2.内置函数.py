# 数据处理管道
def process_data(data):
    # 过滤有效数据
    valid_data = list(filter(lambda x: x is not None and x > 0, data))
    # 数据转换
    process_data = list(map(lambda x: x * 2, valid_data))
    # 排序
    sorted_data = sorted(process_data)
    # 统计
    stats = {
        "count": len(sorted_data),
        "sum": sum(sorted_data),
        "max": max(sorted_data) if sorted_data else 0,
        "min": min(sorted_data) if sorted_data else 0,
    }
    return sorted_data, stats


# 使用示例
raw_data = [1, 2, None, 3, -1, 4, 0, 5]
processed, stats = process_data(raw_data)
print(f"处理后的数据: {processed}")
print(f"统计信息: {stats}")
