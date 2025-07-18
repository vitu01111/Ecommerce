from flask import render_template, Blueprint, request, redirect, flash, url_for
from src.Models.Slide import Slider
from src.db import db
from werkzeug.utils import secure_filename
import os
from src.Administrator.Slider.form import SliderForm
slider_bp = Blueprint('slider', __name__)

IMAGE_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@slider_bp.route('/')
def slider():
    sliders = db.session.query(Slider).order_by(Slider.id).all()
    form = SliderForm()
    return render_template('admin/slider/index.html', slider=sliders,form=form)

@slider_bp.route('/create', methods=['GET', 'POST'])
def createForm():
    form=SliderForm()
    if request.method == 'POST':
        name = request.form.get('name')
        image = request.files.get('image')
        image_filename = ""
        if image and image.filename and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(IMAGE_FOLDER, image_filename)
            # os.makedirs(IMAGE_FOLDER, exist_ok=True)
            image.save(image_path)
        new_slider = Slider(name=name, image=image_filename)
        db.session.add(new_slider)
        db.session.commit()
        flash("Slider created successfully", 'success')
        return redirect(url_for('slider.slider'))
    return render_template('admin/slider/add.html',form=form)

@slider_bp.route('/edit/<int:slider_id>', methods=['GET', 'POST'])
def editForm(slider_id):
    slider = Slider.query.get_or_404(slider_id)
    form=SliderForm(obj=slider)
    if request.method == 'POST':
        name = request.form.get('name')
        image = request.files.get('image')
        slider.name = name
        if image and image.filename and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(IMAGE_FOLDER, image_filename)
            # os.makedirs(IMAGE_FOLDER, exist_ok=True)
            image.save(image_path)
            slider.image = image_filename
        db.session.commit()
        flash("Slider updated successfully", 'success')
        return redirect(url_for('slider.slider'))
    return render_template('admin/slider/edit.html', slider=slider,form=form)

@slider_bp.route('/delete/<int:delete_id>', methods=['POST'])
def deleteSlider(delete_id):
    slider = Slider.query.get_or_404(delete_id)
    # form=SliderForm()
    db.session.delete(slider)
    db.session.commit()
    flash("Slider deleted successfully", 'success')
    return redirect(url_for('slider.slider'))