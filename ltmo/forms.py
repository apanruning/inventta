from ltmo.models import Leak
from flaskext.fungiform import Form, TextField, CommaSeparated
     
class LeakForm(Form):
    description = TextField('description')
    tags = CommaSeparated(TextField('tag'))
    author = TextField('author')
    
    
