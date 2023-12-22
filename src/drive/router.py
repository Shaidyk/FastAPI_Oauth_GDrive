import config

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from drive import drive_utils
from auth.base_config import templates
from main import logger

router = APIRouter(
    prefix='',
    tags=['auth']
)


@router.get('/drive')
def drive(request: Request):
    logger.info(f"User {request.session['user']['email']} get Drive")
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')

    creds = config.get_creds(request.session['user']['email'])
    items = drive_utils.all_drive(creds)
    logger.info(f"User {request.session['user']['email']} get drive items")
    return templates.TemplateResponse(
        name='drive.html',
        context={
            'request': request,
            'user': user,
            'items': items[:10]
        }
    )


@router.get('/download')
def create_folder(request: Request, file_id: str):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')

    if not user:
        return RedirectResponse('/')

    creds = config.get_creds(request.session['user']['email'])
    drive_utils.download_file(creds, file_id)
    logger.info(f"User {request.session['user']['email']} download files")
    return RedirectResponse('/drive')