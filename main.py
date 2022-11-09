from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) #cannot include anything without name
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

### to be used only one time, after server ran
#db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

#Each of those can be updated
video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")

### below was for tests how works, before interaction with database
#videos = {}

# def abort_if_video_not_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="Couldn't found video...")
#
# def abort_if_video_exist(video_id):
#     if video_id in videos:
#         abort(409, message="Video already exist with that id...")
###

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer,
}

class Video(Resource):
    @marshal_with(resource_fields) #decorator, create dicionary with id, name, view information, serialize
    def get(self, video_id):
        #abort_if_video_not_exist(video_id)
        #return videos[video_id]
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Couldn't find video with that ID")
        return result

    @marshal_with(resource_fields) #serialize
    def put(self, video_id):
        # abort_if_video_exist(video_id)
        # args = video_put_args.parse_args()
        # videos[video_id] = args
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video ID taken")

        ### values goes into VideoModel
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        ### add model to the session
        db.session.add(video)
        db.session.commit()
        #return videos[video_id], 201
        return video, 201

    ### update by standard command patch
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video dosent exist, cannot update")

        #return f"Video has been updated of +{name}, {views}, {likes}", 204

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.name = args['views']
        if args['likes']:
            result.name = args['likes']

        db.session.commit()

        return result

    def delete(self, video_id):
        abort_if_video_not_exist(video_id)
        del videos[video_id]
        return "Video has been removed", 204

api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True)