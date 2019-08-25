from rest_api import db
from .models import Load, CitizensSchema, Person, PersonSchema, person_patch_schema
from flask_marshmallow.sqla import ValidationError
from flask import jsonify
from .utils import execute_sql, check_sql_has_result
from .sql_queries import *
from numpy import percentile
import timeit


def save(in_json):
    try:
        load = Load()
        citizens, errors = CitizensSchema().load(in_json)
        if errors:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp

        check_citizens = {}
        db.session.add(load)

        for person in citizens["citizens"]:
            person.load = load
            check_citizens[person.citizen_id] = person, set(person.relatives)

        for check_person in check_citizens:
            check_person_relatives = check_citizens[check_person][1]
            for candidate in check_person_relatives:
                if not check_citizens[candidate]:
                    raise ValidationError('Error no relatives')
                else:
                    if check_citizens[check_person][0].citizen_id not in check_citizens[candidate][1]:
                        raise ValidationError('Error no relatives')

        db.session.commit()
        db.session.bulk_save_objects(citizens["citizens"], return_defaults=True)
        resp = jsonify({"data": {"import_id": load.id}})
        resp.status_code = 201

    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400

    return resp


def update(in_json, import_id, citizen_id):
    try:
        # 1 - проверка данных по схеме
        income_person, errors = person_patch_schema().load(in_json)
        if errors:
            raise ValidationError(errors)
        income_person.citizen_id = citizen_id
        income_person.load_id = import_id

        # 2 - проверка - существует такой import и citizen_id
        person = Person.query.filter_by(load_id=import_id, citizen_id=citizen_id).first()
        if person is None:
            raise ValidationError('There is no data')

        # 3 - обновление данных
        # обновляем все поля, кроме relatives
        person_fields = Person.all_fields()
        person_fields.remove('relatives')
        for field in person_fields:
            next_field_value = getattr(income_person, field)
            if next_field_value:
                setattr(person, field, next_field_value)

        if income_person.relatives:
            update_relatives(income_person, person)

        db.session.add(person)
        db.session.commit()

        # формирование выходного результата
        result = PersonSchema().dump(person)
        resp = jsonify({"data": result.data})
        resp.status_code = 200

    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp

    return resp


def update_relatives(income_person, real_person):
    # Определение добавленных, удаленных родственных связей
    add_relatives = set(income_person.relatives).difference(set(real_person.relatives))
    minus_relatives = set(real_person.relatives).difference(set(income_person.relatives))
    real_person.relatives = income_person.relatives

    # 1 - Добавление родственных связей
    for citizen in add_relatives:
        if citizen == real_person.citizen_id:
            continue
        relative_person = Person.query.filter_by(load_id=real_person.load_id, citizen_id=citizen).first()
        if not relative_person:
            raise ValidationError('Relatives has inappropriate records')
        relative_person.relatives = relative_person.relatives + [real_person.citizen_id]
        db.session.add(relative_person)

    # 2 - Удаление родственных связей
    for citizen in minus_relatives:
        if citizen == real_person.citizen_id:
            continue
        relative_person = Person.query.filter_by(load_id=real_person.load_id, citizen_id=citizen).first()
        if not relative_person:
            raise ValidationError('Relatives has inappropriate records')
        updated_relatives = set(relative_person.relatives)
        updated_relatives.remove(real_person.citizen_id)
        relative_person.relatives = updated_relatives
        db.session.add(relative_person)


def get_import_data(import_id):
    try:
        # 1 - проверка, есть ли у нас эти данные
        all_person = Person.query.filter_by(load_id=import_id).all()
        if all_person is None:
            raise ValidationError('There is no data')

        # 2 - формирование выходного результата
        result = PersonSchema(many=True).dump(all_person)
        resp = jsonify({"data": result.data})
        resp.status_code = 200
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp

    return resp


def get_birthday_stat(import_id):
    try:
        # 1 - проверка, есть ли у нас эти данные
        check_person = Person.query.filter_by(load_id=import_id).first()
        if check_person is not None:
            raise ValidationError('There is no data')

        # 2 - наполнение данных
        stat = {str(i): [] for i in range(1, 12 + 1)}
        result = execute_sql(birthday_stat_sql(import_id))
        for i in result:
            citizen_id, month, presents = i
            add_data = {"citizen_id": citizen_id, "presents": presents}
            stat[str(int(month))].append(add_data)

        # 3 - формирование выходного результата
        resp = jsonify({"data": stat})
        resp.status_code = 200

    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp

    return resp


def get_age_stat(import_id):
    try:
        # 1 - проверка, есть ли у нас эти данные
        check_person = Person.query.filter_by(load_id=import_id).first()
        if check_person is not None:
            raise ValidationError('There is no data')

        # 2 - наполнение данных
        stat = []
        towns_stat = execute_sql(age_by_town_stat_sql(import_id))
        for town in towns_stat:
            name, ages = town
            pers_stat = percentile(ages, q=[50, 75, 99], interpolation='linear')
            town_stat = {
                            "town": name,
                            "p50": pers_stat[0],
                            "p75": pers_stat[1],
                            "p99": pers_stat[2],
                        }
            stat.append(town_stat)
        # 3 - формирование выходного результата
        resp = jsonify({"data": stat})
        resp.status_code = 200

    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp

    return resp