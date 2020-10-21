from datetime import datetime

from flask import current_app as app

from app.main import bp


@bp.route('/<toc_id>')
def index(toc_id):
    results = app.es.get(index='toc', id=toc_id)
    return results

@bp.route('/toc/<bookid>')
def toc(bookid):
    results = app.es.search(
        index='toc',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.bookid': bookid}},
                        {'match': {'doc.display': True}}
                    ]
                }
            },
            'size': 10000,
            'sort': ['doc.open']
        }
    )
    # get rid of the es cruft
    results = results['hits']['hits']
    tocs = [t['_source']['doc'] for t in results]
    return {'results': tocs}
