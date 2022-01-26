from setup_db import db
from flask import request
from models import Book
from flask_restx import Namespace, Resource

book_ns = Namespace('books')


@book_ns.route('/')
class BooksView(Resource):
    def get(self):
        result = Book.query.all()
        res = []
        for book in result:
            sm_d = book.__dict__
            del sm_d['_sa_instance_state']
            res.append(sm_d)
        return res, 200

    def post(self):
        req_json = request.json
        entity = Book(**req_json)

        db.session.add(entity)
        db.session.commit()
        return "", 201


@book_ns.route('/<int:rid>')
class BookView(Resource):
    def get(self, bid: int):
        review = Book.query.get(bid)
        sm_d = review.__dict__
        del sm_d['_sa_instance_state']
        return sm_d, 200

    def put(self, bid: int):
        review = Book.query.get(bid)
        req_json = request.json
        review.user = req_json.get("user")
        review.rating = req_json.get("rating")
        review.book_id = req_json.get("book_id")

        db.session.add(review)
        db.session.commit()
        return "", 204

    def delete(self, bid: int):
        review = Book.query.get(bid)

        db.session.delete(review)
        db.session.commit()
        return "", 204
