from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import os
import random
import time

views = Blueprint('views', __name__)

# Static Pages --------------------------------------------------------

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/about', methods=['GET'])
def about():
    return render_template("about.html", user=current_user)


@views.route('/faq', methods=['GET'])
def faq():
    return render_template("faq.html", user=current_user)


# Application Forms --------------------------------------------------------

@views.route('/loans', methods=['GET'])
def loans():
    return render_template("loans.html", user=current_user)


@views.route('/loans_apply', methods=['GET', 'POST'])
def loans_apply():
    return render_template("loans_apply.html", user=current_user)


@views.route('/mortgages', methods=['GET'])
def mortgages():
    return render_template("mortgages.html", user=current_user)


@views.route('/mortgages_apply', methods=['GET', 'POST'])
def mortgages_apply():
    return render_template("mortgages_apply.html", user=current_user)


@views.route('/credit', methods=['GET'])
def credit():
    return render_template("credit.html", user=current_user)


@views.route('/credit_apply', methods=['GET', 'POST'])
def credit_apply():
    return render_template("credit_apply.html", user=current_user)


@views.route('/business', methods=['GET'])
def business():
    return render_template("business.html", user=current_user)


@views.route('/business_apply', methods=['GET', 'POST'])
def business_apply():
    return render_template("business_apply.html", user=current_user)



# Accounts -----------------------------------------------------------------------

@views.route("/accounts", methods=['GET', 'POST'])
@login_required
def accounts():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json/" + str(current_user.email) + "_account.json")
    data = json.load(open(json_url))
    # work out total for current account
    current_account_total = 0
    for p in data['current_account']:
        current_account_total += float(p['Amount'])

    # work out total for savings account
    savings_account_total = 0
    for p in data['savings_account']:
        savings_account_total += float(p['Amount'])

    # work out total for investments account
    investments_account_total = 0
    for p in data['investments_account']:
        investments_account_total += float(p['Amount'])

    current_account_total = "{0:,.2f}".format(current_account_total)
    savings_account_total = "{0:,.2f}".format(savings_account_total)
    investments_account_total = "{0:,.2f}".format(investments_account_total)

    return render_template('accounts.html', data=data, current_account_total=current_account_total, savings_account_total=savings_account_total, investments_account_total=investments_account_total, user=current_user)


@views.route("/current", methods=['GET', 'POST'])
@login_required
def current():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json/" + str(current_user.email) + "_account.json")
    data = json.load(open(json_url))
    # work out total
    current_account_total = 0
    for p in data['current_account']:
        current_account_total += float(p['Amount'])
        p['Amount'] = "{0:,.2f}".format(float(p['Amount']))

    current_account_total = "{0:,.2f}".format(current_account_total)
    return render_template('current.html', data=data, current_account_total=current_account_total, user=current_user)


@views.route("/savings", methods=['GET', 'POST'])
@login_required
def savings():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json/" + str(current_user.email) + "_account.json")
    data = json.load(open(json_url))
    # work out total
    savings_account_total = 0
    for p in data['savings_account']:
        savings_account_total += float(p['Amount'])
        p['Amount'] = "{0:,.2f}".format(float(p['Amount']))

    savings_account_total = "{0:,.2f}".format(savings_account_total)
    return render_template('savings.html', data=data, savings_account_total=savings_account_total, user=current_user)


@views.route("/investments", methods=['GET', 'POST'])
@login_required
def investments():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/json/" + str(current_user.email) + "_account.json")
    data = json.load(open(json_url))
    # work out total
    investments_account_total = 0
    for p in data['investments_account']:
        investments_account_total += float(p['Amount'])
        p['Amount'] = "{0:,.2f}".format(float(p['Amount']))

    investments_account_total = "{0:,.2f}".format(investments_account_total)
    return render_template('investments.html', data=data, investments_account_total=investments_account_total, user=current_user)


@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)
