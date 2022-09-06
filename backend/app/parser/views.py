from flask import Blueprint, abort, jsonify, request
from bs4 import BeautifulSoup
from flair.data import Sentence
from flair.models import SequenceTagger
import requests

model = SequenceTagger.load("ner_model/best-model.pt")
parse = Blueprint('api/parse', __name__, url_prefix='/api/parse')


@parse.route('', methods=['GET'])
def get():
    url = request.args.get("url")
    if not url:
        abort(400)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    content = soup.find('title')
    if not content:
        return jsonify({})
    text = content.text
    se = Sentence(text)
    model.predict(se)

    data = {}
    for entity in se.get_spans('ner'):
        entity_value = entity.get_label("ner").value
        entity_score = entity.get_label("ner").score
        if entity_value == 'JOB':
            if 'position' not in data or 'position' in data and entity_score > data['position'][1]:
                data['position'] = (entity.text, entity_score)
        if entity_value == 'ORG':
            if 'company' not in data or 'company' in data and entity_score > data['company'][1]:
                data['company'] = (entity.text, entity_score)

    print(data)
    return jsonify(data)

