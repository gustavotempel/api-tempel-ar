from tempel.web import create_app
from dotenv import load_dotenv

from tempel.conf import Settings

load_dotenv()

settings = Settings()

app = create_app(settings)

app.debug = True

# Start the application
app.run()