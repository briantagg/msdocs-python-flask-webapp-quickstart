from flask import Blueprint, render_template, request, flash, json, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import os
import random
import time

admin = Blueprint('admin', __name__)

# Static Pages --------------------------------------------------------

@admin.route('/admin', methods=['GET', 'POST'])
def home():
    return render_template("admin.html", user=current_user)
