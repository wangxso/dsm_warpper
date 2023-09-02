import requests
from flask import Flask, request
from api import system

session = requests.session()

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return system.DSMLogin(username, password)

@app.route("/logout", methods=['GET'])
def logout():
    return system.DSMLogout()

@app.route("/info", methods=['GET'])
def info():
    return system.DSMInfo()

@app.route("/status", methods=['GET'])
def status():
    return system.DSMStatus()

@app.route("/network", methods=['GET'])
def network():
    return system.DSMNetwork()

@app.route("/service", methods=['GET'])
def service_info():
    return system.DSMService()

@app.route("/terminal", methods=['POST'])
def terminal_setting():
    data = request.get_json()
    enablessh = data['enablessh']
    enabletelnet = data['enabletelnet']
    sshport = data['sshport']
    return system.DSMTerminal(enablessh, enabletelnet, sshport)



if __name__ == "__main__":
    app.run()