from bottle import run, view, post, get, request, redirect
from lunch import dals_list, sabzis_list, sweets_list

@route('/hello/<name>')
@view('index')
def index(name):
    return dict(name=name)
 


@get('/chowhound/submit')
@view('form')
def data():


    return dict(dals = dals_list, sabzis = sabzis_list, sweets=sweets_list, suggested = [])
    

@post('/submit')
def submit():
    chosen_dal = request.forms.get('Dal')
    chosen_sabzi = request.forms.get('Sabzi')
    chosen_sweet = request.forms.get('Sweets')
    waste = request.forms.get('waste')

    chosen_menu = { 'dal':chosen_dal, 'sabzi': chosen_sabzi, 'sweet':chosen_sweet }
    print(chosen_menu)
    print(waste)
    redirect('/chowhound/submit')



run(host='localhost', port=8080, reloader=True)