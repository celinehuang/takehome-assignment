from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/shows", methods=["GET"])
def get_all_shows():

    # check if there a query
    min_episode = request.args.get("minEpisodes")
    all_shows = db.get("shows")
    if min_episode is not None:
        filterd_shows = [
            show for show in all_shows if show["episodes_seen"] >= int(min_episode)
        ]

        # filterd_shows = []
        # for show in all_shows:
        #     if show["episodes_seen"] >= int(min_episode):
        #         filterd_shows.append(show)

        return create_response({"shows": filterd_shows})
    return create_response({"shows": all_shows})


@app.route("/shows/<id>", methods=["DELETE"])
def delete_show(id):
    if db.getById("shows", int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.deleteById("shows", int(id))
    return create_response(message="Show deleted")


# TODO: Implement the rest of the API here!


@app.route("/shows/<id>", methods=["GET"])
def get_by_id(id):
    if db.getById("shows", int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    db.getById("shows", int(id))
    return create_response({"shows": db.getById("shows", int(id))})


@app.route("/shows", methods=["POST"])
def create_show():
    response = request.json
    try:
        name = response["name"]
        episodes_seen = response["episodes_seen"]

        if not isinstance(episodes_seen, int):
            raise ValueError

        db.create("shows", response)
        return create_response(status=201, message=response["name"])

    except KeyError as error:
        return create_response(status=422, message="Parameter(s) is missing")
    except ValueError as error:
        return create_response(status=422, message="Invalid value")


@app.route("/shows/<id>", methods=["PUT"])
def update_show(id):
    new_response = request.json
    if db.getById("shows", int(id)) is None:
        return create_response(status=404, message="No show with this id exists")
    item = db.updateById("shows", int(id), new_response)
    return create_response(status=201, message=new_response["name"])


"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
