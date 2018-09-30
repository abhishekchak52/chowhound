from bottle import run, view, post, get, request, response, redirect, template
from lunch import dals_list, sabzis_list, sweets_list
from mess_env import serve
from web_app_policy import *

chosen_menu = serve()

@get('/submit')
@view('form')
def data():

    suggested = [request.cookies.get('dal'), request.cookies.get('sabzi'), request.cookies.get('sweet')]

    return dict(dals = dals_list, sabzis = sabzis_list, sweets=sweets_list, suggested = suggested if suggested else [])
    

@post('/submit')
def submit():
    chosen_dal = request.forms.get('Dal')
    chosen_sabzi = request.forms.get('Sabzi')
    chosen_sweet = request.forms.get('Sweets')
    waste = request.forms.get('waste')


    chosen_menu = { 'dal':chosen_dal, 'sabzi': chosen_sabzi, 'sweet':chosen_sweet }
    response.set_cookie('dal', chosen_dal)
    response.set_cookie('sabzi', chosen_sabzi)
    response.set_cookie('sweet', chosen_sweet)
    
    print(chosen_menu)
    print(waste)
    redirect('/submit')



run(host='localhost', port=8080, reloader=True)