from src.Models.Image import Image
from src.db import db
import os 
from werkzeug.utils import secure_filename
from flask import Blueprint,render_template,redirect,url_for,request,flash


image_bp=Blueprint('image',__name__)

STORE_FOLDER='static/uploads'
ALLOWED_EXTENSIONS={'png','jpg','jpeg','git'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@image_bp.route('/image',methods=['GET'])
def image():
    image=db.session.query(Image).order_by(Image.id).all()
    
    
    return render_template('web/image/image_list.html',image=image)


@image_bp.route('/showImage',methods=['GET'])
def showImage():
    return render_template('web/image/image_add.html')


@image_bp.route('/addImage',methods=['POST'])
def addImage():
    image=request.files.get('image')
    image_filename=""
    if image and image.filename:
        if allowed_file(image.filename):
            image_filename=secure_filename(image.filename)
            image_path=os.path.join(STORE_FOLDER,image_filename)
            image.save(image_path)
    new_image=Image(image=image_filename)
    db.session.add(new_image)
    db.session.commit()
    flash('image uploaded successfully','success')
    return redirect(url_for('image.image'))


@image_bp.route('/edit/<int:image_id>',methods=['GET'])
def editImage(image_id):
    image=Image.query.get_or_404(image_id)
    return render_template('web/image/image_edit.html',image=image)
@image_bp.route('/editData/<int:image_id>', methods=['POST'])
def editDataForm(image_id):
    image = Image.query.get_or_404(image_id)
    image_file = request.files.get('image')
    if image_file and image_file.filename:
        if allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(STORE_FOLDER, image_filename)
            image_file.save(image_path)
            image.image = image_filename  # Save only the filename in the database
    db.session.commit()
    flash('Image updated successfully', 'success')
    return redirect(url_for('image.image'))
@image_bp.route('/delete/<int:image_id>',methods=['POST'])
def deleteImage(image_id):
    image_id=Image.query.get_or_404(image_id)
    db.session().delete(image_id)
    db.session.commit()
    return redirect(url_for('image.image'))    
        
            