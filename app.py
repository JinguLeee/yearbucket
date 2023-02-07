from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.1ktc4ez.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    comment_receive = request.form['comment_give']

    result = 'success'
    msg = '저장되었습니다.'

    if comment_receive == '':
        msg = '버킷리스트를 입력해주세요';
        result = 'fail'

    if result != 'fail':
        bucket_list = list(db.yearbucket.find({}, {'_id': False}))
        count = len(bucket_list) + 1

        doc = {
            'num':count,
            'comment':comment_receive,
            'done':0
        }
        db.yearbucket.insert_one(doc)

    return jsonify({'msg':msg, 'result':result})

@app.route("/bucket", methods=["GET"])
def bucket_show():
    bucket_list = list(db.yearbucket.find({}, {'_id': False}))
    return jsonify({'buckets':bucket_list})

@app.route("/update/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    bucket_list = db.yearbucket.find_one({'num': int(num_receive)}, {'_id': False})

    if bucket_list['done'] == 0:
        done = 1
    else:
        done = 0

    db.yearbucket.update_one({'num': int(num_receive)}, {'$set': {'done': done}})
    return jsonify(None)

@app.route("/update/show", methods=["POST"])
def update_show():
    num_receive = request.form['num_give']
    print(num_receive)
    bucket_list = db.yearbucket.find_one({'num':int(num_receive)}, {'_id': False})
    return jsonify({'buckets':bucket_list})

@app.route("/update/save", methods=["POST"])
def update_save():
    comment_receive = request.form['comment_give']
    num_receive = request.form['num_give']

    result = 'success'
    msg = '저장되었습니다.'

    if comment_receive == '':
        msg = '버킷리스트를 입력해주세요';
        result = 'fail'
    else:
        bucket_list = db.yearbucket.find_one({'num': int(num_receive)}, {'_id': False})
        if comment_receive == bucket_list['comment']:
            msg = '수정하실 버킷리스트를 입력해주세요';
            result = 'fail'

    if result != 'fail':
        db.yearbucket.update_one({'num':int(num_receive)},{'$set':{'comment':comment_receive}})

    return jsonify({'msg':msg, 'result':result})

@app.route("/update/del", methods=["POST"])
def update_del():
    num_receive = request.form['num_give']
    print(num_receive)
    db.yearbucket.delete_one({'num':int(num_receive)})
    return jsonify(None)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)