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
    upvote = request.args.get('upvote')
    downvote = request.args.get('downvote')
    print("Upvote:", upvote, " Downvote:", downvote)
    if not query:
        data = []
    else:
        if upvote:
            upvote_recipe(upvote)
        elif downvote:
            downvote_recipe(downvote)

        if top_k(query, omits, 100) == "No results found":
            data = "EMPTY"
        else:
            data = top_k(query, omits, 12)
    return render_template('search.html', name=project_name, netid=net_id, query=query, omits=omits, data=data)
