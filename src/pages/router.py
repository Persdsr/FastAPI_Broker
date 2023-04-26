from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from operations.router import get_specific_operations

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')

@router.get('/base')
def get_base_page(request: Request):
    return templates.TemplateResponse('search.html', {'request': request})


@router.get('/search/{operation_type}/')
def get_base_page(request: Request, operations=Depends(get_specific_operations)):
    return templates.TemplateResponse('search.html', {'request': request, 'operations': operations})


@router.get('/chat')
def get_page_chat(request: Request):
    return templates.TemplateResponse('chat.html', {'request': request})