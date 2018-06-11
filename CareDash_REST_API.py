from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import create_engine
import os

app = Flask(__name__)
# engine = create_engine('mysql://care:dash@localhost/caredashdb')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://care:dash@localhost/caredashdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Doctor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(60), unique=True, nullable=False)
	reviews = db.relationship('Review',backref='doctor',lazy=True)
	def __repr__(self):
		return f"User('{self.id}','{self.name}')"

class Review(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	review_id = db.Column(db.Integer, unique=False)
	description = db.Column(db.String(300), nullable=False)
	doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

	def __repr__(self):
		return f"Review('{self.id}','{self.review_id}','{self.description}')"

class DoctorSchema(ma.ModelSchema):
	class Meta:
		model = Doctor

class ReviewSchema(ma.ModelSchema):
	class Meta:
		model = Review

db.create_all()


@app.route('/doctors',methods=['POST'])
def create_doctor():
	json_request = request.json
	doctor = Doctor(name=json_request['doctor']['name']);
	db.session.add(doctor)
	try:
		db.session.commit()
		return jsonify({'message':'New doctor created'})
	except IntegrityError:
		return jsonify({'message': 'Dr.' + doctor.name + ' already exists'})

@app.route('/doctors',methods=['GET'])
def get_doctors():
	all_doctors = Doctor.query.all()
	results = []; 
	for doctor in all_doctors:
		result = {'name':doctor.name,'id':doctor.id, 'reviews' :[]}
		for review in doctor.reviews:
			# result.append({'name':doctor.name, 'id':doctor.id, 'reviews': doctor.reviews})
			result["reviews"].append({"id":review.id,"doctor_id":review.doctor_id,"description":review.description})
		results.append(result)
	return jsonify(results)

@app.route('/doctors/<int:doctor_id>',methods=['GET'])
def get_doctor(doctor_id):
	try: 
		doctor = Doctor.query.filter_by(id=doctor_id).first()
		result = {'name':doctor.name,'id':doctor.id, 'reviews' :[]}
		for review in doctor.reviews:
			result["reviews"].append({"id":review.review_id,"doctor_id":review.doctor_id,"description":review.description})
		return jsonify(result)
	except AttributeError:
		return jsonify({'message':'doctor does not exist'})

@app.route('/doctors/<int:doctor_id>/reviews', methods=['POST'])
def create_review(doctor_id):
	json_request = request.json
	review = Review(description=json_request['review']['description'][0:-9], review_id = int(json_request['review']['description'][-1]), doctor_id=doctor_id)
	db.session.add(review)
	db.session.commit()
	return jsonify({'message':'New review created'})

@app.route('/doctors/<int:doctor_id>/reviews', methods=['GET'])
def get_reviews(doctor_id):
	reviews = Review.query.filter_by(doctor_id= doctor_id).all()
	results = []
	if (len(reviews) != 0):
		for review in reviews:
			result = {'description':review.description, 'id':review.review_id, 'doctor_id':review.doctor.id, 'doctor':{'id':review.doctor.id, 'name':review.doctor.name}}
			results.append(result)
		return jsonify(results)
	else:
		return jsonify({'message':'review does not exist for this doctor'})

@app.route('/doctors/<int:doctor_id>/reviews/<int:review_id>', methods=['GET'])
def get_review(doctor_id,review_id):
	try: 
		review = Review.query.filter_by(review_id = review_id, doctor_id = doctor_id).first()
		result = {'description':review.description, 'id':review.review_id, 'doctor_id':review.doctor.id, 'doctor':{'id':review.doctor.id, 'name':review.doctor.name}}
		return jsonify(result)
	except AttributeError:
		return jsonify({'message':'review does not exist'})

@app.route('/doctors/<int:doctor_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(doctor_id,review_id):
	review = Review.query.filter_by(doctor_id = doctor_id, review_id = review_id).first()
	db.session.delete(review)
	db.session.commit()
	return jsonify({'message':'Review deleted'})

@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
	doctor = Doctor.query.filter_by(id = doctor_id).first()
	db.session.delete(doctor)
	db.session.commit()
	return jsonify({'message':'Doctor deleted'})



if __name__ == "__main__":
	app.run(host = 'localhost',port = 3000, debug = True)

	





