from flask import Blueprint
from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


businessBlueprint = Blueprint('business', __name__)

@businessBlueprint.route('/api/businesses', methods=['POST'])
def createBusiness():
    global BUSINESSES
    global loggedInUser    
    # bus = Business(1232312, 'name', 'location', 'category', 'description')    
    jsn= request.data
    data = json.loads(jsn)
    busx = Business(str(uuid4()), data['name'], loggedInUser[0], data['location'], data['category'], data['description'])
    res = busx.createBusiness(str(uuid4()), data['name'], loggedInUser[0], data['location'], data['category'], data['description'])
    
    if res:
        return jsonify({'message': 'Business successfully created'})
    else:
        return jsonify({'message':'Business was not created, Try again!!'})


@businessBlueprint.route('/api/businesses/<string:id>', methods=['GET'])
def getOneBusiness(id):
    global BUSINESSES
    # bus = Business(1232312, 'name', 'location', 'category', 'description')

    if not BUSINESSES:
        return jsonify({'message':'No records of any Business Exist.'})
    else:
        result = Business.checkBusinessExists(id)
        if result or result == 0:
            return jsonify({'business':BUSINESSES[result]})
        else:
            return jsonify({'business':'No Records of that business Exists'})
    


@businessBlueprint.route('/api/businesses', methods=['GET'])
def getAllBusinesses():
    global BUSINESSES
    if not BUSINESSES:
        return jsonify({'message':'No records found. Register a business'})
    else:        
        return jsonify({'Businesses': BUSINESSES})

@businessBlueprint.route('/api/businesses/<string:id>', methods=['PUT'])
def updatebusiness(id):
    global BUSINESSES
    # bus = Business(1232312, 'name', 'location', 'category', 'description')
    if BUSINESSES:
        jsn= request.data
        data = json.loads(jsn)
        exists = Business.checkBusinessExists(id)
        busId = ''

        if exists or exists == 0:           
            # print(BUSINESSES[exists])
            res = BUSINESSES[exists] # lets get
            for k, v in res.items():
                busId = k
            
            BUSINESSES[exists] = {busId : [data['name'], loggedInUser[0], data['location'], data['category'], data['description']]}
            return jsonify({'business': exists, 'businesses': BUSINESSES})
        else:
            return jsonify({'message': 'no records of that business exists', 'exists':exists})

        
@businessBlueprint.route('/api/businesses/<string:id>', methods=['DELETE'])
def deletebusiness(id):
    global BUSINESSES    

    if BUSINESSES:        
        result = Business.deleteBusiness(id)
        # print(result)
        if result or result == 0:
            BUSINESSES.pop(result)
            return jsonify({'message':'Business has been successfully deleted'}), 200
        else:
            return jsonify({'message':'No business has that id, nothing was deleted.'}), 404
    else:
        return jsonify({'message': 'No records of any Business Exist.'}), 404