import config

from authlib.integrations.base_client import OAuthError
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from auth.base_config import oauth, templates
from main import logger

router = APIRouter(
    prefix='',
    tags=['auth']
)


async def get_current_user_token(request: Request):
    token = await oauth.google.authorize_access_token(request)
    return token


@router.get('/')
def get_base_page(request: Request):
    logger.info("Processing root request")
    if request.session.get('user'):
        logger.info("Redirect user '/' -> 'welcomr'")
        return RedirectResponse('welcome')
    return templates.TemplateResponse('landing.html', {'request': request})


@router.get('/login')
async def login(request: Request):
    logger.info("Processing login request")
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get('userinfo')
        request.session['user'] = dict(user)
        config.get_creds(request.session['user']['email'])
        logger.info(f"User {request.session['user']['email']} authenticated")
    except OAuthError as e:
        request.session.clear()
        logger.error(f"Error {e}")
        return RedirectResponse('/')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)

    return RedirectResponse('welcome')


@router.get('/logout')
def logout(request: Request):
    logger.info(f"User {request.session['user']['email']} logout")
    request.session.pop('user')
    return RedirectResponse('/')


@router.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return templates.TemplateResponse(
        name='welcome.html',
        context={
            'request': request,
            'user': user
        }
    )



