from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *


project_name = "Let's Get This Bread"
net_id = "Lindsey Luo: lgl47, Thomas Lu: tlu398, Michelle Loven: ml2359, Peter Munn: pcm82"


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    omits = request.args.get('omit')
    if not query:
        data = []
    else:
        if top_k(query, omits, 100) == "No results found":
            data = "EMPTY"
        else:
            top_k_output = top_k(query, omits, 12)
            data = top_k_output[1]
            updated_query = top_k_output[0]
    return render_template('search.html', name=project_name, netid=net_id, query=query, omits=omits, data=data, updated_query=updated_query)
