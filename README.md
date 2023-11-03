

Clue-Less WebApp
Description:
This web application allows users to play a game based on "Clue". Users can register, log in, create lobbies, join lobbies, and communicate via chat.

Prerequisites
Install Python:
Ensure Python is installed. If not, download it from Python's official website.

Install Virtual Environment:
python -m pip install virtualenv

Install Flask and Flask-SocketIO:
pip install Flask Flask-SocketIO

Setup and Installation

Set Up a Virtual Environment:
python -m venv venv

Activate the Virtual Environment:

On macOS and Linux:
source venv/bin/activate
On Windows:
.\venv\Scripts\Activate

Install the Required Packages:
pip install -r requirements.txt

Running the Application

Set Flask Environment Variable:
export FLASK_APP=app
Run the Application:
flask run
Access in Browser:
Visit http://127.0.0.1:5000/.

Known Issues
403 Error: If you encounter a 403 error, fully close Chrome and reopen it.
