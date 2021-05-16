import datetime
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ResourcesModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    contact = db.Column(db.String(25), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    msg = db.Column(db.String(50))
    resource_type = db.Column(db.Integer, nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"Resource-> id={self.id}, name={self.name}, contact={self.contact}, resource_type={self.resource_type}"

#db.create_all()

resource_cv100_put_args = reqparse.RequestParser()
resource_cv100_put_args.add_argument('name', type=str, help='Enter the contact\'s name.')
resource_cv100_put_args.add_argument('contact', type=str, help='Enter the contact information.', required=True)
resource_cv100_put_args.add_argument('date', type=inputs.datetime_from_iso8601, help='Enter the date.', required=True)
resource_cv100_put_args.add_argument('resource_type', type=int, help='Enter the resource_type.', required=True)
resource_cv100_put_args.add_argument('upvotes', type=int, help='Enter the number of upvotes.')
resource_cv100_put_args.add_argument('downvotes', type=int, help='Enter the number of downvotes.')
resource_cv100_put_args.add_argument('msg', type=str, help='Enter a message.')

resource_cv100_update_args = reqparse.RequestParser()
resource_cv100_update_args.add_argument('name', type=str, help='Enter the contact\'s name.')
resource_cv100_update_args.add_argument('contact', type=str, help='Enter the contact information.')
resource_cv100_update_args.add_argument('date', type=inputs.datetime_from_iso8601, help='Enter the date.')
resource_cv100_update_args.add_argument('resource_type', type=int, help='Enter the resource_type.')
resource_cv100_update_args.add_argument('upvotes', type=int, help='Enter the number of upvotes.')
resource_cv100_update_args.add_argument('downvotes', type=int, help='Enter the number of downvotes.')
resource_cv100_update_args.add_argument('msg', type=str, help='Enter a message.')

resource_fields = {
    'id':fields.Integer,
    'name':fields.String,
    'contact':fields.String,
    'date':fields.DateTime,
    'msg':fields.String,
    'resource_type':fields.String,
    'upvotes':fields.Integer,
    'downvotes':fields.Integer
}

class Resource_cv100(Resource):

    #@marshal_with(resource_fields)
    def put(self, resource_id):
        args = resource_cv100_put_args.parse_args()
        result = ResourcesModel.query.filter_by(id=resource_id).first()
        if result:
            abort(409, message='This ID is already taken.')
        
        resource=ResourcesModel(id=resource_id,
                                name=args['name'],
                                contact=args['contact'], 
                                date=args['date'],
                                resource_type=args['resource_type'], 
                                upvotes=args['upvotes'],
                                downvotes=args['downvotes'],
                                msg=args['msg'])
        db.session.add(resource)
        db.session.commit()

        return 'Put successful', 201

    @marshal_with(resource_fields)
    def get(self, resource_id):
        result = ResourcesModel.query.filter_by(id=resource_id).first()
        if not result:
            abort(404, message='Resource with this ID does not exist. Could not get')

        return result

    #@marshal_with(resource_fields)
    def patch(self, resource_id):
        args = resource_cv100_update_args.parse_args()
        result = ResourcesModel.query.filter_by(id=resource_id).first()
        if not result:
            abort(404, message='Resource with that ID does not exist. Could not update')

        if args['name']:
            result.name = args['name']

        if args['contact']:
            result.contact = args['contact']
        
        if args['date']:
            result.date = args['date']

        if args['resource_type']:
            result.resource_type = args['resource_type']

        if args['upvotes']:
            result.upvotes = args['upvotes']

        if args['downvotes']:
            result.downvotes = args['downvotes']

        if args['msg']:
            result.msg = args['msg']

        db.session.commit()
        return 'Update successful'

    #@marshal_with(resource_fields)
    def delete(self, resource_id):
        result = ResourcesModel.query.filter_by(id=resource_id).first()
        temp = result
        if not result:
            abort(404, message='Resource with that ID does not exist. Could not delete.')

        db.session.delete(result)
        db.session.commit()
        return 'Delete successful', 204

class  AllResources(Resource):
    @marshal_with(resource_fields)
    def get(self) -> list:
        result = ResourcesModel.query.all()
        return result

# ==
# ===
# =>
# ==>

# Member data for covid 100 collaborators, leaving it hardcoded for now.
members_data = {
    1:{'name':'Amar pratap singh', 'role':'Machine learning engineer'},
    2:{'name':'Kshitij kumar', 'role':'Android developer'}
    }

# Resource for members of the project.
class Members(Resource):
    def get(self, member_id):
        return members_data[member_id]

api.add_resource(Members, '/member/<int:member_id>')
api.add_resource(Resource_cv100, '/resource/<int:resource_id>')
api.add_resource(AllResources, '/all_resource')

if __name__ == '__main__':
    app.run(debug=True)
