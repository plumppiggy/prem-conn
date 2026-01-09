# Premier League Connections

This is a fun and simple game deployed here : https://plumppiggy.github.io/prem-conn

The crossword page is in progress.


### Development

#### Starting Crossword Server

```powershell
cd crossword
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn server:app --reload --port 8801
```

#### Starting the React App

```powershell
npm install

npm start
```