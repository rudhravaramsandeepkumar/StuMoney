import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file, make_response, \
    Response, jsonify
from sqlalchemy.orm.exc import NoResultFound
import threading
from . import APP, LOG
from werkzeug.utils import secure_filename
from .security.updated_jwt import jwt_required
import time
from .models import db
from .models.UserCredentials import UserCredentials
from .helpers import get_random_numbers, validate_gmail
from datetime import datetime
from portal.packages import Get_One_Year_Data,get_cal_

bp = Blueprint('view', __name__, url_prefix='/', template_folder="./templates", static_folder="./static")




@bp.route('/', methods=["GET", "POST"])
def homePage():
    return render_template('LandingPage.html')




@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        invalid_msg = "hidden"
        access_name = "hidden"
        access_pass = "hidden"
        pedning_approved = 'hidden'
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass,
                               pedning_approved=pedning_approved)
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '':
            invalid_msg = "hidden"
            access_name = ""
            access_pass = "hidden"
            pedning_approved = 'hidden'
            return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass, pedning_approved=pedning_approved)
        if password == '':
            invalid_msg = "hidden"
            access_name = "hidden"
            access_pass = ""
            pedning_approved = 'hidden'
            return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name,
                                   access_pass=access_pass, pedning_approved=pedning_approved)
        try:
            users = UserCredentials.query.filter_by(username=username, password=password).one()
            user_id_get = users.user_uid
            if users is not None:
                if users.active == 'y':
                    session["user"] = username
                    session["role"] = users.attributes_1
                    session["user_uid"] = users.user_uid
                    session["id"] = users.Id
                    session["display_name"] = users.username
                    return render_template("home2.html")
            pass
        except Exception as e:
            LOG.error("Error occurred while login ")
            LOG.error(e, exc_info=True)
        finally:
            db.session.close()
        invalid_msg = ""
        access_name = "hidden"
        access_pass = "hidden"
        pedning_approved = 'hidden'
        return render_template("login.html", invalid_msg=invalid_msg, access_name=access_name, access_pass=access_pass,
                               pedning_approved=pedning_approved)


@bp.route('/check', methods=["GET", "POST"])
def enc_key():
    data = request.json
    print(data)
    reg_username = data['reg_username']
    reg_email = data['reg_email']
    print(data)
    try:
        users = UserCredentials.query.filter_by(username=reg_username).one()
        print(users.username)
        msg = ''
        if users is not None:
            msg = "user_name"
            return jsonify({"msg": msg})
    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while login ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    try:
        users2 = UserCredentials.query.filter_by(email_id=reg_email).one()
        if users2 is not None:
            msg = "email_id"
            return jsonify({
                "msg": msg})
        else:
            msg = "clear"
            return jsonify({
                "msg": msg})
    except NoResultFound:
        pass
    except Exception as e:
        LOG.error("Error occurred while login ")
        LOG.error(e, exc_info=True)
    finally:
        db.session.close()
    Status = {"msg": "msg"}
    return jsonify(Status)


@bp.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return render_template("home2.html")
    else:
        return render_template("home2.html")


@bp.route('/registration', methods=['POST'])
def registration():
    if request.method == "POST":
        data = request.json
        if not (len(data['reg_username']) <= 50):
            msg = "User name is too long"
            Status = {"status": msg}
            return jsonify(Status)
        if not validate_gmail(data['reg_email']):
            msg = "Invalid Gmail"
            Status = {"status": msg}
            return jsonify(Status)
        header_id = datetime.now().strftime("%d%m%Y%H%M%S") + get_random_numbers(5)
        head = UserCredentials(user_uid=header_id,
                               password=data['reg_password'],
                               username=data['reg_username'],
                               email_id=data['reg_email'],
                               active='y',
                               status='pending admin approval',
                               attributes_1='user')
        try:
            db.session.add(head)
            db.session.commit()
            db.session.close()
            msg = "successfully registered"
            Status = {"status": msg}
            print('Status', Status)
            return jsonify(Status)
        except Exception as e:
            LOG.error(e, exc_info=True)
            db.session.rollback()
            LOG.error("Error while pushing data")
            msg = "Failed"
            Status = {"status": msg}
            return jsonify(Status)


@bp.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":

        final_data_ = {"final_data_": 'mhdbn'}
        return render_template("dashboard.html", final_data_=final_data_)
    else:
        final_data_ = Get_One_Year_Data()
        let_l=["META", "AAPL", "AMZN", "NFLX", "GOOGL"]

        print('final_data_',final_data_)

        return render_template("dashboard.html",final_data_=final_data_)


@bp.route('/get_invert', methods=["GET", "POST"])
def get_invert():
    if request.method == "POST":
        final_data_ = request.json
        Total_Amount_Due=final_data_['Amount_for_']
        print('Total_Amount_Due',Total_Amount_Due)
        period1=final_data_['bdate']
        ticker=final_data_['site']
        period2=final_data_['bdate2']
        Company_name_,start_date,end_date,num_shares_bought,final_investment_value,initial_investment,final_investment_value,value=get_cal_(period1, period2, ticker, Total_Amount_Due)
        final_data_ = Get_One_Year_Data()

        return jsonify(
            {"Company_name_":Company_name_,
             "start_date":start_date,
             "end_date":end_date,
             "num_shares_bought":num_shares_bought,
             "final_investment_value":final_investment_value,
             "initial_investment":initial_investment,
             "value":value}
        )
    # else:
    # #     return render_template("dashboard.html", final_data_=final_data_)
    # else:
    #     final_data_ = Get_One_Year_Data()
    #     let_l=["META", "AAPL", "AMZN", "NFLX", "GOOGL"]
    #
    #     print('final_data_',final_data_)
    #
    #     return render_template("dashboard.html",final_data_=final_data_)


@bp.route('/leaderboard', methods=["GET", "POST"])
def leaderboard():
    return render_template("LeaderBoard.html")