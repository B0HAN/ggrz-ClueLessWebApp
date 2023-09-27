print("Starting run.py")
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Running Flask app...")
    app.run(debug=True)
print("Finished run.py")
