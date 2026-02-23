from app import create_app
from dotenv import load_dotenv
import os

# add variables (your real apis / database password .etc) from .env 
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
