import fpdf

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mysql/app'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/', methods=['POST'])
def index():
    first_name = request.json['first-name']

    user = User.query.filter_by(first_name=first_name)

    if not user:
        return jsonify({'result': False})

    create_user_pdf(user)

    return jsonify({'result': True})


def create_user_pdf(user: User):
    # Create PDF
    pdf = fpdf.FPDF(format='letter')
    pdf.add_page()

    # Setup Font
    pdf.set_font("Arial", size=12)

    # Add Image from File
    pdf.image('{}.jpg'.format(user.id), 0, 0, 200, 200)

    # Add Text
    pdf.cell(300, 10, txt=user.first_name)
    pdf.cell(300, 10, txt=user.last_name)

    # Write PDF
    pdf.output('{}.pdf'.format(user.id))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
