import argparse, json, os, re
from urllib import request
from app import create_app
from flask import current_app
from elasticsearch import helpers


ESDB = 'http://es01:9200'


def getfiles(directory):
    with open(f'{directory}/text.json') as fin:
        text = json.load(fin)
    with open(f'{directory}/annotations.json') as fin:
        annotations = json.load(fin)
    return text, annotations


def insertdata(text, annotations, update):
    app = create_app()
    with app.app_context():
        actions = []
        for t in text:
            actions.append({
                '_index': 'text',
                '_id': f'{t["bookid"]}-{t["sequence"]}',
                'doc': t,
                '_op_type': 'update' if update else 'index'
            })
        for a in annotations:
                actions.append({
                    '_index': a['type'],
                    '_id': f'{a["bookid"]}-{a["id"]}',
                    'doc': a,
                    '_op_type': 'update' if update else 'index'
                })
        result = helpers.bulk(current_app.es, actions)
    return result


def main(din, update):
    # poll the es db until it responds
    i = 0
    while True:
        try:
            if not i % 1000:
                print(f"Request {i}", flush=True)
            i += 1
            request.urlopen(ESDB)
        except:
            if not i % 1000:
                print("...nope", flush=True)
            continue
        print("Success.", flush=True)
        break

    for d in os.listdir(din):
        if re.match(r'[0-9]+-', d):
            text, annotations = getfiles(f'{din}/{d}')
            result = insertdata(text, annotations, update)
            print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert text.json and"
                                     "annotations.json files in the es db.")
    parser.add_argument('din', metavar='dirin', nargs='?', type=str,
                        help="The directory containing the text.json file"
                        "and the annotations.json file.")
    parser.add_argument('-u', '--update', action='store_true',
                        help="Update the index instead of just inserting (for"
                        "when the items already exist).")
    args = parser.parse_args()
    main(args.din, args.update)
