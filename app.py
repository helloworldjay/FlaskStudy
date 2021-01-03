from flask import Flask, request, jsonify

app = Flask(__name__)
app.users = {}  # 가입한 사용자 저장 key = id: int, value = new_user: JSON
app.id_count = 1


@app.route("/ping", methods=['GET'])
def ping() -> str:
    return "pong"


# 회원가입
@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user = request.json  # JSON -> dict
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count + 1
    return jsonify(new_user)  # dict -> JSON


# 트윗 구현
app.tweets = []


@app.route('/tweet', methods=['POST'])
def tweet() -> tuple:
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "사용자가 존재하지 않습니다", 400

    if len(tweet) > 300:
        return "300자를 초과했습니다", 400

    user_id = int(payload['id'])
    app.tweets.append({
        "user_id": user_id,
        "tweet": tweet
    })

    return '', 200


# 팔로우, 언팔로우
@app.route('/follow', methods=['POST'])
def follow():
    payload = request.json
    user_id = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자가 존재하지 않습니다", 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)

    return jsonify(user)
