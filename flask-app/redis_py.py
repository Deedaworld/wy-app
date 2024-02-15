from flask import Flask, jsonify, request
import redis
from flask_cors import CORS
from awsConfig import get_dynamodb_resource

app = Flask(__name__)
CORS(app,supports_credentials=True)

redis_host = 'init-test.tfsu7r.ng.0001.apn2.cache.amazonaws.com'
redis_port = 6379

dynamodb = get_dynamodb_resource()
table = dynamodb.Table('init-db')

@app.route('/ticket')
def hello_fnc():
    r = redis.Redis(host=redis_host, port=redis_port)
    value = r.lpop("A-sector")
    if value:
        seat_id = value.decode('utf-8')
        return jsonify({"seat_id": seat_id})
    else:
        return jsonify({"error": "No data available"})



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
        value = r.lpop("A-sector")
        print("Value from Redis:", value)
        
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
