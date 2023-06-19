from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["MSEARCH_INDEX_NAME"] = "msearch"
app.config["MSEARCH_BACKEND"] = "whoosh"
app.config["MSEARCH_ENABLE"] = True


db = SQLAlchemy(app)
search = Search(app, db=db)


class Message(db.Model):
    __tablename__ = "messages"
    __searchable__ = ["text"]

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)


@app.get("/search")
def search_message() -> Response:
    query = request.args.get('query')
    if not query:
        return abort(400)

    messages = Message.query.msearch(query).all()
    return jsonify(
        {
            "messages": [message.text for message in messages],
        },
    )


@app.post("/message")
def create_messages() -> Response:
    messages = request.json["messages"]

    for message in messages:
        db.session.add(Message(text=message))

    db.session.commit()
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
