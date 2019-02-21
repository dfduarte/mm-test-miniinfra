from flask import Flask
from flask import request
from aws_sqs import aws_sqs_create_message

 
app = Flask(__name__)
 
@app.route('/suggestions', methods = ['POST'])
def postJsonHandler():
    content = request.get_json()
    if 'suggestion' not in content:
        return 'Please, post a valid json! - It must contain a suggestion key and a String value'
    else:
        print(content['suggestion'])
        aws_sqs_create_message(content['suggestion'])
        return 'JSON ok! - If you are seeing this, then everything went fine!'

@app.route('/', methods = ['GET'])
def fallbackHandler():
    return 'Please, use /suggestions endpoint with a POST method as specified'

if __name__ == '__main__':
 
     app.run(host='0.0.0.0', port= 8090)
     