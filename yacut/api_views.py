from flask import request, jsonify

from http import HTTPStatus

from yacut import app
from yacut.error_handlers import (InvalidAPIUsage, InvalidLength,
                                  InvalidRegex, EmploymentShortId,
                                  ErrorGenerations)
from yacut.models import (URLMap, INVALID_SHORT_ID, EMPLOYMENT_SHORT_ID,
                          ERROR_GENERATIONS)

REQUEST_EMPTY = 'Отсутствует тело запроса'
MISSING_REQUIRED_FIELD_URL = '"url" является обязательным полем!'
ERROR_SHORT_ID = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_new_short_link():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(REQUEST_EMPTY)
    if 'url' not in data:
        raise InvalidAPIUsage(MISSING_REQUIRED_FIELD_URL)
    try:
        url_map = URLMap.create_link(
            data.get('url'), data.get('custom_id'), validate=True
        )
    except (InvalidLength, InvalidRegex):
        raise InvalidAPIUsage(INVALID_SHORT_ID)
    except EmploymentShortId:
        raise InvalidAPIUsage(
            EMPLOYMENT_SHORT_ID.format(short=data.get('custom_id'))
        )
    except ErrorGenerations:
        raise InvalidAPIUsage(ERROR_GENERATIONS)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short_link(short_id):
    object_url_map = URLMap.get(short_id)
    if not object_url_map:
        raise InvalidAPIUsage(ERROR_SHORT_ID, HTTPStatus.NOT_FOUND)
    return jsonify(url=object_url_map.original), HTTPStatus.OK
