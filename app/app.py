from flask import Flask, render_template, request
from flask_restful import Resource, Api

from utils import writeJson

from table import Table

from datetime import datetime



app = Flask(__name__)
api = Api(app)


@app.route('/')
def index():
    return render_template('index.html')


class IndexAPIView(Resource):

    def get_predicate(self, predicate, value):
        if predicate == "contains":
            return f"LIKE  '%{value}%'"
        if predicate == "not_equals":
            return f"!= '{value}'"
        if predicate == "less_than":
            value = f"{datetime.now()}"
            return f"< '{value}'"
        return f"LIKE  '%{value}%'"


    def post(self):

        data  = request.form
        data = data.to_dict(flat=True)


        WHERE = ""

        WHERE += f"{data['field']} {self.get_predicate(data['predicate'], data['value1'])}"

        WHERE += " AND " if data["predicates"] == "all" else " OR "

        WHERE += f"{data['field2']} {self.get_predicate(data['predicate2'], data['value2'])}"

        # WHERE += " AND " if data["predicates"] == "all" else " OR "

        # WHERE += f"{data['field3']} {self.get_predicate(data['predicate3'], data['value3'])}"

        table = Table()

        # if table is created
        # Filter queryset
        if table.create_table() and table.query_set(WHERE):
            # if query exists create rules
          
            writeJson("rules.json", data)

            return {"message": "Rules created"}

        return {"message": "Rules does not match"}


api.add_resource(IndexAPIView, '/')



if __name__ == '__main__':
    app.run(debug=True)