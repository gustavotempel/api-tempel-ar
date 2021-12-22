from dotenv import load_dotenv

from tempel.conf import Settings
from tempel.web import create_app

load_dotenv()

settings = Settings()

app = create_app(settings)

app.debug = True

# Start the application
if __name__ == '__main__':
    app.run()
