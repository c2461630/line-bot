from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace with your LINE Channel Access Token
LINE_ACCESS_TOKEN = "e37a143ce3fd34e995d2caa67d82cbef"

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

previous_point_difference_frequency = 0

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    for event in data["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_id = event["source"]["userId"]
            message_text = event["message"]["text"]
            if message_text.lower() == 'exit':
                reply_message = "退出遊戲"
            else:
                player_points = message_text
                broker_points = "5 6 7"  # Replace with broker's points or use user input

                player_points = [convert_card_value(card) for card in player_points.split()]
                broker_points = [convert_card_value(card) for card in broker_points.split()]

                player_total = calculate_total(player_points)
                broker_total = calculate_total(broker_points)

                diff = calculate_diff(player_total, broker_total)
                frequency_value = calculate_frequency_value(diff)

                player_pattern_flow, broker_pattern_flow = calculate_pattern_flow(player_points, broker_points)

                point_difference_frequency = calculate_point_difference_frequency(frequency_value, player_pattern_flow, broker_pattern_flow)

                result = determine_next_superiority(point_difference_frequency)

                oscillation_amplitude = abs(previous_point_difference_frequency) - abs(point_difference_frequency)
                if oscillation_amplitude >= 10:
                    result += "\n震盪幅度過大，可以考慮反打"

                oscillation_amplitude = abs(point_difference_frequency) - abs(previous_point_difference_frequency)
                if oscillation_amplitude >= 10:
                    result += "\n震盪幅度過大，可以考慮反打"

                previous_point_difference_frequency = point_difference_frequency

            send_reply_message(user_id, result)
    return "OK"

def send_reply_message(user_id, message):
    import requests
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
    }
    data = {
        "replyToken": user_id,
        "messages": [{"type": "text", "text": message}],
    }
    response = requests.post(
        "https://api.line.me/v2/bot/message/reply", json=data, headers=headers
    )

if __name__ == "__main__":
    app.run()