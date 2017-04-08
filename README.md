# power-rangers
Suncode 2017 Hackathon

## Setup
Make sure to have [nodejs](https://nodejs.org/en/download/) installed.

### Set up backend
From project root:
```sh
pip install -r requirements.txt
```

### Set up frontend
From project root:
```sh
npm install -g bower
cd app/static && bower install
```

## Start the server
From project root:
```sh
python run.py runapp --debug
```

Visit <https://localhost:8080/index.html> in your browser.