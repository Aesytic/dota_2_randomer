import uvicorn
import sys
import os

from api.main import app

sys.path.insert(0, os.getcwd())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")
