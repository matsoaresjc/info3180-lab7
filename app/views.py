"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request,jsonify,flash
from werkzeug.utils import secure_filename
from forms import UploadForm
import os

###
# Routing for your application.
###


@app.route('/')
def index():
    """Render website's initial page and let VueJS take over."""
    return render_template('index.html')
    

@app.route('/api/upload',methods=['POST'])
def upload():
     # Instantiate your form class
    img = UploadForm()
    # Validate file upload on submit
    if request.method == 'POST' and img.validate_on_submit():
        # Get file data and save to your uploads folder
        #img_data = request.files['img_data']
        img_data = img.photo.data
        description = img.description.data
        filename = secure_filename(img_data.filename)
        try:
            img_data.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return jsonify(message = "File Upload Successful",filename = filename, description = description)
        except Exception as e:
            print e
            return jsonify(errors = ["internal error"])
    return jsonify(errors = form_errors(img))        
        
     


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
