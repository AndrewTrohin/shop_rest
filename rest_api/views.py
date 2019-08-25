from rest_api import app, controllers
from flask import request


@app.route("/imports", methods=["POST"])
def import_citizens():
    return controllers.save(request.json)


@app.route("/imports/<int:import_id>/citizens/<int:citizen_id>", methods=["PATCH"])
def update_citizen(import_id, citizen_id):
    return controllers.update(request.json, import_id, citizen_id)


@app.route("/imports/<int:import_id>/citizens", methods=["GET"])
def get_import_data(import_id):
    return controllers.get_import_data(import_id)


@app.route("/imports/<int:import_id>/citizens/birthdays", methods=["GET"])
def get_birthday_stat(import_id):
    return controllers.get_birthday_stat(import_id)


@app.route("/imports/<int:import_id>/stat/percentile/age", methods=["GET"])
def get_age_stat(import_id):
    return controllers.get_age_stat(import_id)