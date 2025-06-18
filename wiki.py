import logging
from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Setup logger
logger = logging.getLogger('Wiki')
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wiki.db'
db = SQLAlchemy(app)

# Resource field for Documents
document_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'latest_version_id': fields.Integer
}

# Resource field for Versions
version_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'timestamp': fields.DateTime,
    'timestamp_simple': fields.Integer
}


# Define a class for the Document table
class DocumentModel(db.Model):
    __tablename__ = 'documents'
    # Primary key of Document
    id = db.Column('id', db.Integer, primary_key=True)
    # Title of Document
    title = db.Column('title', db.String(50), unique=True)
    # Latest Version ID for the Document
    latest_version_id = db.Column('latest_version_id', db.Integer, db.ForeignKey('versions.id'))


# Define a class for the Version table
class VersionModel(db.Model):
    __tablename__ = 'versions'
    # Primary key of Version
    id = db.Column(db.Integer, primary_key=True)
    # Title of Version corresponding Document
    title = db.Column('title', db.String(50), db.ForeignKey('documents.title'))
    # Content of Version, Text stores up to 8000 characters
    content = db.Column('content', db.Text)
    # Timestamp uploaded in datetime form
    timestamp = db.Column(db.DateTime(timezone=True))
    # Simple version of timestamp, in the form HHMM
    timestamp_simple = db.Column(db.Integer)


# Corresponds to /documents calls
class DocumentVersions(Resource):
    def get(self):
        logger.info('Getting document titles...')
        result_rows = DocumentModel.query.with_entities(DocumentModel.title).all()
        result_str = [str(row.title) for row in result_rows]
        logger.debug('Document titles: [{}]'.format(result_str))
        return result_str


# Corresponds to /documents/<string:title> calls
class DocumentTitle(Resource):
    @marshal_with(version_resource_fields)
    def get(self, title):
        # Get all versions of a document from it's title
        versions = VersionModel.query.filter_by(title=title).all()
        return versions

    @marshal_with(document_resource_fields)
    def post(self, title):
        content = request.form['content']
        version = VersionModel(title=title, content=content, timestamp=datetime.now(),
                               timestamp_simple=int('{}{}'.format(datetime.now().hour, datetime.now().minute)))
        db.session.add(version)
        db.session.commit()

        # Check if document title exists
        document = DocumentModel.query.filter_by(title=title).first()
        if document is not None:
            # Update document's latest version id if it already exists
            document.latest_version_id = version.id

        else:
            # Set Documents version id to created Version's ID
            document = DocumentModel(title=title, latest_version_id=version.id)
            db.session.add(document)
        db.session.add(document)
        db.session.commit()

        return document     # TODO: Return JSON of document and version


# Corresponds to /documents/<string:title>/latest calls
class LatestDocument(Resource):
    @marshal_with(version_resource_fields)
    def get(self, title):
        # Get latest Version of Document using latest_version_id field
        document = DocumentModel.query.filter_by(title=title).first()
        if document:
            latest_version_id = document.latest_version_id
            latest_version = VersionModel.query.filter_by(id=latest_version_id).first()
        else:
            return None
        return latest_version


# Corresponds to /documents/<string:title>/<int:timestamp> calls
class TimestampDocument(Resource):
    @marshal_with(version_resource_fields)
    def get(self, title, timestamp):
        # Get Document Version from simple timestamp (just uses hours and minutes)
        # TODO: Implement datetime string parser so we can use time AND date to find version
        # TODO: Add validation for invalid timestamps
        results = VersionModel.query.filter_by(title=title)\
            .with_entities(VersionModel.id, VersionModel.timestamp_simple).all()

        if results:
            for result in results:
                version_id = result[0]
                version_timestamp = result[1]
                version = None
                if timestamp <= version_timestamp:
                    version = VersionModel.query.filter_by(id=version_id).first()
                    break

            if not version:
                version = VersionModel.query.filter_by(id=version_id).first()

        else:
            return None

        return version


# Create tables and database
db.create_all()
api = Api(app)

# Add routes to API
api.add_resource(DocumentVersions, '/documents')
api.add_resource(DocumentTitle, '/documents/<string:title>')
api.add_resource(LatestDocument, '/documents/<string:title>/latest')
api.add_resource(TimestampDocument, '/documents/<string:title>/<int:timestamp>')

if __name__ == '__main__':
    app.run(debug=True)     # TODO: Remove debug mode before finishing

# TODO:
#  Improve validation, need figure out how to do error handling with 'marshal_with'
#  Improve logging
#  Add more unit tests
#  Flesh out README
