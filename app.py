from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

members_data = {
    1:{'name':'Amar pratap singh', 'role':'Machine learning engineer'},
    2:{'name':'Kshitij kumar', 'role':'Android developer'},
    3:{'name':'Khush malawaliya', 'role':'Full stack web developer'}}

class Members(Resource):
    def get(self, member_id):
        return members_data[member_id]

api.add_resource(Members, '/member/<int:member_id>')

if __name__ == '__main__':
    app.run(debug=True)