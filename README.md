# power-rangers
Suncode 2017 Hackathon

## Setup
Make sure to have [nodejs](https://nodejs.org/en/download/) installed.

### Set up backend
*From project root:*
```sh
pip install -r requirements.txt
```

### Set up frontend
*From project root:*
```sh
npm install -g bower
cd app/static && bower install
```

## Start the server
*From project root:*
```sh
python run.py runapp --debug --port=8888
```
The port number is arbitrary. It just needs to not already be in use. 

Once the server is running, visit <http://localhost:8888/index.html> in your browser.
