from collections import defaultdict
import os
from typing import Tuple

from flask import Flask, render_template, request, session

from escape_room.admin.crm import bp as crm_blueprint
from escape_room.enums import ItemStatus, Status
from escape_room.login import login_manager
from escape_room.models import Item, Room, User
from escape_room.wrappers import content

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")
app.register_blueprint(crm_blueprint, url_prefix="/crm")
login_manager.init_app(app)

def get_item(item_name: str | None) -> Tuple[Status, Item | ItemStatus]:
    if not item_name:
        return (Status.FAIL, ItemStatus.NO_ITEM_GIVEN)

    item_count = player.location.inventory.get(Item(name=item_name))
    item = item_lookup.get(item_name)
    if not item_count or not item:
        return (Status.FAIL, ItemStatus.NO_ITEM_FOUND)

    player.location.inventory[item] -= 1

    return Status.SUCCESS, item


@app.route('/drop', methods=["POST"])
@content
def drop_item():
    item_name = request.form.get("item_name", "").lower()

    if item_name not in item_lookup or not player.inventory.get(item_lookup[item_name], None):
        return f"You don't have any {item_name}"

    player.inventory[item_lookup[item_name]] -= 1
    player.location.inventory[item_lookup[item_name]] += 1

    return f"Dropped {item_name}"

@app.route("/look")
@content
def look():
    draw_inventory = sum([x for x in player.location.inventory.values()])
    return render_template(
        'room.jinja',
        room=player.location,
        draw_inventory=draw_inventory
    )

@app.route('/wait')
@content
def wait_turn():
    return "You let time pass."


@app.route("/get", methods=["POST"])
@content
def pickup_item():
    item_name = request.form.get("item_name", "").lower()
    status, item = get_item(item_name)

    if status == Status.FAIL:
        if item == ItemStatus.NO_ITEM_GIVEN:
            return "Get what item?"
        if item == ItemStatus.NO_ITEM_FOUND:
            return f"Could not find {item_name}."

    assert isinstance(item, Item), "somehow item is not an Item :("

    if status == Status.SUCCESS:
        if item in player.inventory and player.inventory[item] > 0:
            if item.bulky:
                return f"It is too dificult to carry more than one {item.name}!"
        if item not in player.inventory:
            player.inventory[item] = 1
        else:
            player.inventory[item] += 1

        return f"Added {item.name} to your inventory!"

    return f"could not find that item"


@app.route("/inventory", methods=["GET"])
@content
def inventory():
    draw_inventory = sum(player.inventory.values())
    return render_template(
        "inventory.jinja",
        inventory=player.inventory,
        draw_inventory=draw_inventory
    )


@app.route("/", methods=["GET"])
def index():
    if "player" not in session:
        session['player'] = player.model_dump_json()
    return render_template("index.html", player=player)


def run():
    print(app.url_map)
    print(app.blueprints)
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    run()
