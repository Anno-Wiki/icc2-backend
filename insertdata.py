import argparse, json, os, re
from app import create_app
from flask import current_app
from elasticsearch import helpers


def getfiles(directory):
    with open(f'{directory}/text.json') as fin:
        text = json.load(fin)
    with open(f'{directory}/annotations.json') as fin:
        annotations = json.load(fin)
    return text, annotations


def insertdata(text, annotations):
    app = create_app()
    with app.app_context():
        actions = []
        for t in text:
            actions.append({
                '_index': 'text',
                '_type': a['type'],
                '_id': f'{t["bookid"]}-{t["sequence"]}',
                '_source': t
            })
        for a in annotations:
            actions.append({
                '_index': 'annotation',
                '_id': f'{a["bookid"]}-{a["id"]}'
            })
        result = helpers.bulk(current_app.es, actions)
    return result


def main(din):
    for d in os.listdir(din):
        if re.match(r'[0-9]+-', d):
            text, annotations = getfiles(d)
            result = insertdata(text, annotations)
            print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert text.json and"
                                     "annotations.json files in the es db.")
    parser.add_argument('din', metavar='dirin', nargs='?', type=str,
                        help="The directory containing the text.json file"
                        "and the annotations.json file.")
    args = parser.parse_args()
    main(args.din)
