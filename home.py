from bottle import run, view, post, get, request, response, redirect, template, route
from lunch import dals_list, sabzis_list, sweets_list
from mess_env import serve, input_vec, generate_menu
from web_app_policy import *


@route('/')
def home():
    training_model, prediction_model = load_models()
    generated_menu = generate_menu(prediction_model.predict(input_vec(serve())))
    print(generated_menu)
    return '<a href="/submit"> Click here to go to form </a>'


@get('/submit')
@view('form')
def data():

    if request.cookies.get('dal'):
        suggested = [request.cookies.get('dal'), request.cookies.get('sabzi'), request.cookies.get('sweet')]
    else: 
        suggested = list(serve().values())
        response.set_cookie('dal', suggested[0])
        response.set_cookie('sabzi', suggested[1])
        response.set_cookie('sweet', suggested[2])


    return dict(dals = dals_list, sabzis = sabzis_list, sweets=sweets_list, suggested = suggested)
    

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
    

    redirect('/submit')



run(host='localhost', port=8080, reloader=True)