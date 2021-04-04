from flask import current_app as app, request
from ..utils import requires_auth

from app.main import bp

@bp.route('/annotate/toc/<toc_id>', methods=['POST'])
@requires_auth
def annotate(toc_id):
    # toc id
    # start
    # end
    # author
    # text
    print("ACCESSED")
    print(request.json)
    return "true"
