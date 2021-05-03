from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.search import *
from app.irsystem.models.imagescraper import *


project_name = "Let's Get This Bread"
net_id = "Lindsey Luo: lgl47, Thomas Lu: tlu398, Michelle Loven: ml2359, Peter Munn: pcm82"


@irsystem.route('/', methods=['GET'])
def search():
    query = request.args.get('search')
    omits = request.args.get('omit')
    upvote = request.args.get('upvote')
    downvote = request.args.get('downvote')
    updated_query = request.args.get('updated_query')
    if not query:
        data = []
        updated_query = "EMPTY"
    else:
        if upvote:
            upvote_recipe(upvote)
        elif downvote:
            downvote_recipe(downvote)
        top_k_output = top_k(query, omits, 12)
        if top_k_output == "No results found":
            data = "EMPTY"
            updated_query = "EMPTY"
        else:
            data = top_k_output[1]
            if top_k_output[0] != []:
                updated_query = top_k_output[0]
            else:
                updated_query = "EMPTY"
    data_image_urls = []
    if not data == "EMPTY":
        for d in data:
            data_image_urls.append(getImageURL(d[1]))
    dlen = len(data)

    return render_template('search.html', name=project_name, netid=net_id, query=query, omits=omits, data=data, updated_query=updated_query, data_image_urls=data_image_urls, dlen=dlen)
