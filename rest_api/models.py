from rest_api import db, ma
from flask_marshmallow.fields import fields
from flask_marshmallow.sqla import ValidationError
from marshmallow import validates, Schema
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY


class Load(db.Model):
    __tablename__ = "load"
    #__table_args__ = {'extend_existing': True}
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Person(db.Model):
    __tablename__ = "person"
    #__table_args__ = {'extend_existing': True}
    #__table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    load_id = db.Column(db.Integer, db.ForeignKey("load.id", ondelete="CASCADE"), nullable=False)
    load = db.relationship('Load', backref=db.backref('load'))#lazy='joined'
    citizen_id = db.Column(db.Integer, index=True, nullable=False)
    town = db.Column(db.String(256), index=True, nullable=False)
    street = db.Column(db.String(120), nullable=False)
    building = db.Column(db.String(120), nullable=False)
    apartment = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    relatives = db.Column(ARRAY(db.Integer))

    @staticmethod
    def all_fields():
        return ['citizen_id', 'town', 'street',
                'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']

        # return ['id', 'load_id', 'citizen_id', 'town', 'street',
        #         'building', 'apartment', 'name', 'birth_date', 'gender', 'relatives']

    def __repr__(self):
        return f"id={self.id},\n" \
               f"load_id={self.load_id},\n" \
               f"citizen_id={self.citizen_id},\n" \
               f"town={self.town},\n" \
               f"street={self.street},\n" \
               f"building={self.building},\n" \
               f"apartment={self.apartment},\n" \
               f"name={self.name},\n" \
               f"birth_date={self.birth_date},\n" \
               f"gender={self.gender},\n" \
               f"relatives={self.relatives},\n"


class BirthDate(fields.Field):
    def _serialize(self, value, *args, **kwargs):
        return value.strftime("%d.%m.%Y")


class PersonSchema(ma.ModelSchema):
    class Meta:
        model = Person
        fields = (Person.all_fields())
    birth_date = BirthDate(attribute="birth_date", required=True)
    @validates('birth_date')
    def validate_age(self, data, **kwargs):
        try:
            datetime.strptime(data, "%d.%m.%Y")
        except ValueError:
            raise ValidationError('Incorrect date')


class CitizensSchema(Schema):
    citizens = fields.Nested(PersonSchema(many=True))


def person_patch_schema():
    person_patch_scheme = PersonSchema()
    for field in person_patch_scheme.fields:
        person_patch_scheme.fields[field].required = False
    return person_patch_scheme


# def init_database():
#     db.create_all()
#
#
# if __name__ == "__main__":
#     init_database()
