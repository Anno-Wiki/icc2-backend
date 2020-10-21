from functools import reduce

from flask import current_app as app

from app.main import bp


@bp.route('/toc/<toc_id>/')
def gettoc(toc_id):
    results = app.es.get(index='toc', id=toc_id)
    return results['_source']['doc']


@bp.route('/toc/<bookid>/all/')
def alltocs(bookid):
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


@bp.route('/toc/<tocid>/next/')
def nexttoc(tocid):
    toc = gettoc(tocid)
    results = app.es.search(
        index='toc',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.bookid': toc['bookid']}},
                        {'match': {'doc.display': True}},
                        {'match': {'doc.parent': toc['parent']}},
                        {'range': {'doc.id': {'gt': toc['id']}}}
                    ]
                }
            },
            'size': 1,
            'sort': ['doc.id']
        }
    )
    return results['hits']['hits'][0]['_source']['doc']


@bp.route('/toc/<tocid>/range/')
def tocrange(tocid):
    toc = gettoc(tocid)
    next = nexttoc(tocid)
    return {'open': toc['open'], 'close': next['open']}


@bp.route('/toc/<tocid>/textblocks')
def gettextblocks(tocid):
    toc = gettoc(tocid)
    range = tocrange(tocid)
    results = app.es.search(
        index='text',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.bookid': toc['bookid']}},
                        {
                            'range':
                            {
                                'doc.offset':
                                {
                                    'lte': range['open'],
                                    'lt': range['close']
                                }
                            }
                        }
                    ]
                }
            }
        }
    )
    # get rid of es cruft
    results = [r['_source']['doc'] for r in results['hits']['hits']]
    return {'results': results}


@bp.route('/toc/<tocid>/raw')
def rawtext(tocid):
    blocks = gettextblocks(tocid)
    range = tocrange(tocid)
    offset = blocks['results'][0]['offset'] # offset is first text block
    range = {k:v-offset for k,v in range.items()} # subtract offset from range
    text = ''.join(a['text'] for a in blocks['results']) # join blocks
    return {'offset': offset, 'text': text[range['open']:range['close']]}
