from asyncio import current_task
import json
from os import wait
import sys
from typing import Union
from flask import Blueprint, Response, request, abort, current_app, jsonify
from flask.views import MethodView
from pydantic import ValidationError
from escape_room.models import Item, engine, Room


bp = Blueprint("crm", __name__)

@bp.errorhandler(Exception)
def base_error_handler(error):
    current_app.logger.exception(error)
    res = {"error": str(error),}
    return Response(status=500, mimetype="application/json", response=json.dumps(res))

@bp.errorhandler(404)
def error_404_handler(error):
    res = {"error": "object not found"}
    return Response(status=404, mimetype="application/json", response=json.dumps(res))

@bp.errorhandler(400)
def error_400_handler(error):
    res = {"error": "bad request"}
    current_app.logger.exception(error)
    return Response(status=400, mimetype="application/json", response=json.dumps(res))

class ItemAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

    def _get_item(self, name):
        item = engine.find_one(
            Model = self.model.name,
            query=(self.model.name == name)
        )
        if item:
            return item.model_dump(mode="json")
        abort(404)

    def get(self, name):
        item= engine.find_one(Model = self.model, query=(self.model.name == name))
        return jsonify(item)

    def patch(self, name):
        item = engine.find_one(Model = self.model, query=(self.model.name == name))
        updated = item.model_copy(update=request.json)
        engine.save(updated)
        return jsonify(updated.model_dump())

    def delete(self, name):
        engine.delete(Model=self.model, query=(self.model.name == name), delete_one=True)
        return "", 204

class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model

    def get(self):
        items = engine.find_many(Model=self.model)
        return [x.model_dump(mode="json") for x in items]

    def post(self):
        try:
            room:Room = self.model.model_validate(request.json)
        except ValidationError:
            abort(400)

        engine.save(room)
        return room.model_dump(mode="json")

def register_api(app, model, name):
    item = ItemAPI.as_view(f"{name}-item", model)
    group = GroupAPI.as_view(f"{name}-group", model)
    app.add_url_rule(f"/{name}/<int:id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)

register_api(bp, Room, 'room')
register_api(bp, Item, 'item')
