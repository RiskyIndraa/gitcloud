from flask import Flask, jsonify

# AWS Elastic Beanstalk expects the application object to be named 'application' by default
application = Flask(__name__)

@application.route('/')
def hello_admin():
    return jsonify({
        "status": "success",
        "message": "Welcome to the Admin Panel API hosted on AWS Elastic Beanstalk!"
    })

@application.route('/health')
def health_check():
    return "OK", 200

if __name__ == "__main__":
    # Settings for local testing
    application.run(debug=True, port=8080)
