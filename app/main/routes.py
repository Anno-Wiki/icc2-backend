from flask import current_app as app

from app.main import bp

from app.models.annotations import Annotation, Edit


def unfold(results):
    """Helper route to unfold es results and dispense with dict cruft"""
    try:
        return [t['_source']['doc'] for t in results['hits']['hits']]
    except:
        return []


@bp.route('/toc/<toc_id>')
def gettoc(toc_id):
    results = app.es.get(index='toc', id=toc_id)
    return results['_source']['doc']


@bp.route('/text/all')
def alltexts():
    results = app.es.search(
        index='toc',
        body={
            'query': {'match': {'doc.depth': 0}}
        }
    )
    return {'results': unfold(results)}


@bp.route('/text/<slug>')
def gettext(slug):
    results = app.es.search(
        index='toc',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.slug': slug}},
                        {'match': {'doc.id': 0}}
                    ]
                }
            }
        }
    )
    try:
        return unfold(results)[0]
    except:
        return {}


@bp.route('/toc/<slug>/all')
def alltocs(slug):
    results = app.es.search(
        index='toc',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.slug': slug}},
                        {'match': {'doc.display': True}}
                    ]
                }
            },
            'size': 10000,
            'sort': ['doc.open']
        }
    )
    return {'results': unfold(results)}


@bp.route('/toc/<tocid>/next')
def nexttoc(tocid):
    """This route is meant to get the next toc given a toc, but I'm not sure how
    robust it is.
    """

    toc = gettoc(tocid)
    results = app.es.search(
        index='toc',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.bookid': toc['bookid']}},
                        {'match': {'doc.display': True}},
                        {'range': {'doc.id': {'gt': toc['id']}}}
                    ]
                }
            },
            'size': 1,
            'sort': ['doc.id']
        }
    )

    return unfold(results)[0]


@bp.route('/toc/<tocid>/range')
def getrange(tocid):
    toc = gettoc(tocid)
    next = nexttoc(tocid)
    return {'open': toc['open'], 'close': next['open']}


@bp.route('/toc/<tocid>/blocks')
def getblocks(tocid):
    toc = gettoc(tocid)
    range = getrange(tocid)
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
    return {'results': unfold(results)}


@bp.route('/toc/<tocid>/raw')
def rawtext(tocid):
    blocks = getblocks(tocid)
    range = getrange(tocid)

    # offset is first text block
    offset = blocks['results'][0]['offset']
    # subtract offset from range
    range = {k:v-offset for k,v in range.items()}
    # join blocks
    text = ''.join(a['text'] for a in blocks['results'])
    return {'offset': range['open'], 'text': text[range['open']:range['close']]}


@bp.route('/toc/<tocid>/tocs')
def gettocs(tocid):
    toc = gettoc(tocid)
    range = getrange(tocid)
    results = app.es.search(
        index='toc',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.bookid': toc['bookid']}},
                        {'match': {'doc.display': True}},
                        {
                            'range':
                            {
                                'doc.open':
                                {
                                    'gte': range['open'],
                                    'lt': range['close']
                                }
                            }
                        }
                    ]
                }
            },
            'size': 10000,
            'sort': ['doc.open']
        }
    )
    return {'results': unfold(results)}


@bp.route('/toc/<tocid>/styles')
def getstyles(tocid):
    toc = gettoc(tocid)
    range = getrange(tocid)
    results = app.es.search(
        index='style',
        body={
            'query': {
                'bool': {
                    'must': [
                        {'match': {'doc.bookid': toc['bookid']}},
                        {
                            'range':
                            {
                                'doc.open':
                                {
                                    'gte': range['open'],
                                    'lt': range['close']
                                }
                            }
                        }
                    ]
                }
            },
            'size': 10000,
            'sort': ['doc.open']
        }
    )
    return {'results': unfold(results)}


@bp.route('/toc/<tocid>/formatted')
def formattedtext(tocid):
    text = rawtext(tocid)
    text, offset = text['text'], text['offset']
    styles = getstyles(tocid)['results']
    tocs = gettocs(tocid)['results']

    # create an inserts dict for inserting the styles
    annotations = styles + tocs
    inserts = {}
    for a in annotations:
        if a['type'] == 'toc':
            open = '<h' + str(a['depth']) + '>'
            close = '</h' + str(a['depth']) + '>'
        else:
            open = '<' + a['tag'] + '>'
            close = '</' + a['tag'] + '>'
        inserts[a['open'] - offset] = open
        inserts[a['close'] - offset] = close

    # insert the styles
    i = 0
    newtext = []
    for key in sorted(inserts):
        newtext.append(text[i:key])
        newtext.append(inserts[key])
        i = key
    newtext.append(text[i:])

    tmp = ''.join(newtext)
    tmp = tmp.split('\n\n')
    for i in range(0, len(tmp)):
        if (not tmp[i].startswith('<')
                or tmp[i].startswith('<i>')
                or tmp[i].startswith('<b>')
                ):
            tmp[i] = '<p>' + tmp[i] + '</p>'

    return {'offset': offset, 'text': ''.join(tmp)}

@bp.route('/annotations/toc/<toc_id>')
def get_annotations(toc_id):
    offsets = getrange(toc_id)
    bookid = toc_id.split('-')[0]
    a_objects = Annotation.query.\
        join(Edit).\
        filter(Annotation.bookid==bookid,
               Edit.open>= offsets['open'],
               Edit.close <= offsets['close']
               ).order_by(Edit.open).all()
    annotations = []
    for a in a_objects:
        annotations.append({
            'id': a.id,
            'open': a.HEAD.open - offsets['open'],
            'close': a.HEAD.close - offsets['open'],
            'text': a.HEAD.text,
            'author': a.author
        })
    return {'annotations': annotations, 'quantity': len(annotations)}
