from ltmo.models import Leak
from flaskext.fungiform import Form, TextField, Multiple, \
     Mapping, IntegerField, CommaSeparated

class LeakForm(Form):
    description = TextField('Description')
    tags = CommaSeparated()
    author = IntegerField()
    
