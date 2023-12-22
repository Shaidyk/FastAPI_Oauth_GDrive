from authlib.integrations.starlette_client import OAuth
from starlette.templating import Jinja2Templates

from config import CLIENT_ID, CLIENT_SECRET

templates = Jinja2Templates(directory='templates')

oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile https://www.googleapis.com/auth/drive',
        'redirect_uri': 'http://localhost:8000/auth',
    }
)

