from flask import Flask, jsonify, request
import redis
from flask_cors import CORS
from awsConfig import get_dynamodb_resource

app = Flask(__name__)
CORS(app, resources={r"/get-seat-data/*": {"origins": "https://www.wouldyou.store"}})

redis_host = '3.34.192.127'

redis_port = 6379

dynamodb = get_dynamodb_resource()
table = dynamodb.Table('init-db')

@app.route('/')
def hello_fnc():
    return 'hello?'

@app.route('/get-seat-data/<sector>/<id>', methods=['GET'])
def get_seat_data(sector, id):
    try:
        # Redis 클라이언트 생성
        r = redis.Redis(host=redis_host, port=redis_port)

        resp = table.get_item(
            Key={
                'users.id': int(id)
            }
        )

        if 'Item' in resp:
            return jsonify({"seat_id": -1})

        # 데이터 가져오기
        value = r.lpop(f"{sector}-sector")

        if value:
            # Redis에서 가져온 데이터
            seat_id = value.decode("utf-8")

            # DynamoDB에 데이터 입력
            putitem = {
                'users.id': int(id),
                'seat_id': seat_id
            }

            print(putitem)

            table.put_item(
                Item=putitem
            )

            return jsonify({"seat_id": seat_id})
        else:
            return jsonify({"seat_id": None})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
