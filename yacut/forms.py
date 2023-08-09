from flask_wtf import FlaskForm
from wtforms import URLField, StringField, SubmitField
from wtforms.validators import (URL, Length, DataRequired, Optional,
                                ValidationError, regexp)

from settings import (REGEX_SYMBOLS_SHORT_ID, MAX_LENGTH_SHORT_ID,
                      MAX_LENGTH_ORIGINAL)
from yacut.models import URLMap, LENGTH_ORIGINAL

URL_FIELD = 'Введите ссылку'
URL_ERROR = 'Некорректная ссылка'
SHORT_ID = 'Введите короткую ссылку'
LENGTH_SHORT_ID = (
    f'Короткая ссылка не может быть длиннее {MAX_LENGTH_SHORT_ID} символов'
)
REQUIRED = 'Обязательное поле'
CREATE = 'Создать'
NAME_EMPLOYMENT = 'Имя {short} уже занято!'
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'


class URLForm(FlaskForm):
    original_link = URLField(
        URL_FIELD,
        validators=[
            DataRequired(REQUIRED),
            URL(require_tld=True, message=URL_ERROR),
            Length(max=MAX_LENGTH_ORIGINAL, message=LENGTH_ORIGINAL)
        ]
    )
    custom_id = StringField(
        SHORT_ID,
        validators=[
            Length(max=MAX_LENGTH_SHORT_ID, message=LENGTH_SHORT_ID),
            regexp(REGEX_SYMBOLS_SHORT_ID, message=INVALID_SHORT_ID),
            Optional(strip_whitespace=False)
        ]
    )
    submit = SubmitField(CREATE)

    @staticmethod
    def validate_custom_id(original_link, short_id):
        if URLMap.get(short_id.data):
            raise ValidationError(NAME_EMPLOYMENT.format(short=short_id.data))
