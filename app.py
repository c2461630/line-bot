def convert_card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    return int(card)

def calculate_total(points):
    total = sum(points)
    if total >= 30:
        return 0
    if total >= 20:
        return total - 20
    if total >= 10:
        return total - 10
    return total

def calculate_diff(player_total, broker_total):
    diff = abs(player_total - broker_total)
    return diff

def calculate_frequency_value(diff):
    if diff in [0, 1, 2, 3, 9]:
        return 6
    if diff in [5, 6, 8]:
        return -6
    if diff in [4, 7]:
        return -5
    return 0

def calculate_pattern_flow(player_values, broker_values):
    player_pattern_flow = sum([1 if value in [1, 2, 8, 9] else -1 if value in [5, 6, 7] else -4 if value in [3, 4] else 0 for value in player_values])
    broker_pattern_flow = sum([1 if value in [1, 2, 8, 9] else -1 if value in [5, 6, 7] else -4 if value in [3, 4] else 0 for value in broker_values])
    return player_pattern_flow, broker_pattern_flow

def calculate_point_difference_frequency(frequency_value, player_pattern_flow, broker_pattern_flow):
    point_difference_frequency = frequency_value + player_pattern_flow + broker_pattern_flow
    return point_difference_frequency

def determine_next_superiority(point_difference_frequency):
    if point_difference_frequency > 0:
        return "下一局優勢為閒家"
    elif point_difference_frequency < 0:
        return "下一局優勢為莊家"
    else:
        return "下一局平局"

# 在程式的開頭定義一個變數來存儲上一局的點差頻率
previous_point_difference_frequency = 0

while True:
    # 輸入閒家點數
    player_points = input("請輸入閒家點數 (用空格分隔) 或輸入 'exit' 退出: ")
    
    if player_points.lower() == 'exit':
        break
    
    # 輸入莊家點數
    broker_points = input("請輸入莊家點數 (用空格分隔) 或輸入 'exit' 退出: ")
    
    if broker_points.lower() == 'exit':
        break

    # 將輸入的點數轉換為整數
    player_points = [convert_card_value(card) for card in player_points.split()]
    broker_points = [convert_card_value(card) for card in broker_points.split()]
    print("\n")

    # 計算總點數
    player_total = calculate_total(player_points)
    broker_total = calculate_total(broker_points)
    print(f"閒家總點數: {player_total}")
    print(f"莊家總點數: {broker_total}")
    print("\n")

    # 計算點差
    diff = calculate_diff(player_total, broker_total)
    print(f"閒家與莊家點差: {diff}")
    print("\n")

    # 計算頻率數值
    frequency_value = calculate_frequency_value(diff)
    print(f"頻率數值: {frequency_value}")
    print("\n")

    # 計算牌型流數
    player_pattern_flow, broker_pattern_flow = calculate_pattern_flow(player_points, broker_points)
    print(f"閒家牌型流數: {player_pattern_flow}")
    print(f"莊家牌型流數: {broker_pattern_flow}")
    print("\n")

    # 計算點差頻率
    point_difference_frequency = calculate_point_difference_frequency(frequency_value, player_pattern_flow, broker_pattern_flow)
    print(f"點差頻率: {point_difference_frequency}")
    print("\n")

    # 確定下一局的優勢
    result = determine_next_superiority(point_difference_frequency)
    print(result)
    print("\n")
    
    # 更新上一局的點差頻率
    previous_point_difference_frequency = point_difference_frequency
    print("\n")
    
    # 檢查震盪幅度是否過大
    oscillation_amplitude = abs(point_difference_frequency - previous_point_difference_frequency)
    if oscillation_amplitude >= 10 or (point_difference_frequency < 0) != (previous_point_difference_frequency < 0):
        print("震盪幅度過大，可以考慮反打")
