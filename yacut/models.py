import random
import re
from datetime import datetime

from flask import url_for

from settings import (MAX_LENGTH_SHORT_ID, LENGTH_SHORT_ID, APPROVED_SYMBOLS,
                      REGEX_SYMBOLS_SHORT_ID, NAME_FUNK_SHORT_ID,
                      MAX_LENGTH_ORIGINAL, QUANTITY_GENERATIONS)
from yacut import db
from yacut.error_handlers import (EmploymentShortId, InvalidRegex,
                                  InvalidLength, ErrorGenerations)

LENGTH_ORIGINAL = f'Превышена длина ссылки в {MAX_LENGTH_ORIGINAL} символов'
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'
EMPLOYMENT_SHORT_ID = 'Имя "{short}" уже занято.'
ERROR_GENERATIONS = 'Не удалось сгенерировать уникальную ссылку.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_ID), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return dict(url=self.original,
                    short_link=URLMap.full_short_id(self.short))

    @staticmethod
    def get(short_id: str):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def _get_uniq_short_id() -> str:
        for _ in range(QUANTITY_GENERATIONS):
            short_id = ''.join(random.choices(APPROVED_SYMBOLS,
                                              k=LENGTH_SHORT_ID))
            if not URLMap.get(short_id):
                return short_id
        raise ErrorGenerations(ERROR_GENERATIONS)

    @staticmethod
    def _validate_original_link(original_link: str):
        if len(original_link) > MAX_LENGTH_ORIGINAL:
            raise InvalidLength(LENGTH_ORIGINAL)

    @staticmethod
    def _validate_short_id(short_id: str):
        if len(short_id) > MAX_LENGTH_SHORT_ID:
            raise InvalidLength(INVALID_SHORT_ID)
        if not re.search(REGEX_SYMBOLS_SHORT_ID, short_id):
            raise InvalidRegex(INVALID_SHORT_ID)
        if URLMap.get(short_id) is not None:
            raise EmploymentShortId(
                EMPLOYMENT_SHORT_ID.format(short=short_id)
            )

    @staticmethod
    def create_link(original_link: str, short_id: str, validate=False):
        if validate:
            URLMap._validate_original_link(original_link)
            if short_id:
                URLMap._validate_short_id(short_id)
        if not short_id:
            short_id = URLMap._get_uniq_short_id()
        url_map = URLMap(original=original_link, short=short_id)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def full_short_id(short_id: str) -> str:
        return url_for(NAME_FUNK_SHORT_ID, short=short_id, _external=True)
