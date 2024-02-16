from flask import Flask, jsonify, request
import redis
from flask_cors import CORS
from awsConfig import get_dynamodb_resource
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app,supports_credentials=True)

redis_host = '3.34.192.127'
redis_port = 6379

dynamodb = get_dynamodb_resource()
table = dynamodb.Table('init-dynamodb')

@app.route('/ticket')
def hello_fnc():
    id = request.args.get('id')
    # r = redis.Redis(host=redis_host, port=redis_port)
    # value = r.lpop("A-sector")
    # if value:
    #     seat_id = value.decode('utf-8')
    #     return jsonify({"seat_id": seat_id})
    # else:
    #     return jsonify({"error": "No data available"})
    try:
    # DynamoDB에서 데이터 조회
        response = table.get_item(
            Key={
                'users.id': int(id)
            }
        )

    # 조회된 데이터가 있는 경우
        if 'Item' in response:
            seat_id = response['Item'].get('seat_id')
            print(response)
            return jsonify({"seat_id": seat_id}), 200
                
        else:
                return jsonify({"error": "Booking info not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-seat-data/<sector>/<id>', methods=['GET'])
def get_seat_data(sector, id):
    try:
        # Redis 클라이언트 생성
        r = redis.Redis(host=redis_host, port=redis_port)

        # resp = table.get_item(
        #     Key={
        #         'users.id': int(id)
        #     }
        # )

        # if 'Item' in resp:
        #     return jsonify({"seat_id": -1})

        # 데이터 가져오기
        value = r.lpop(f"{sector}-sector")
        print("Value from Redis:", value)
        
        if value:
            # Redis에서 가져온 데이터
            seat_id = value.decode("utf-8")

            # # DynamoDB에 데이터 입력
            # putitem = {
            #     'users.id': 62,
            #     'seat_id': seat_id
            # }

            # print(putitem)

            # table.put_item(
            #     Item=putitem
            # )

            return jsonify({"seat_id": seat_id})
        else:
            return jsonify({"seat_id": None})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
