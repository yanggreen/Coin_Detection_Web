from flask import Flask, request, abort,redirect,url_for,send_from_directory,render_template,make_response
import os
import json
import os
#from split_image import split
from ob_id_image import identification
from werkzeug.utils import secure_filename
import base64
#
if not os.path.exists('images'):
    os.makedirs('images')
    print('create')

app = Flask(__name__)
UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/store")
def hello():
    return "Hello World!"

@app.route('/', methods=['GET'])
def index():
    return render_template('serving_template.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)     
      
@app.route('/image', methods=['POST'])
def image_post():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename ="part_image.png"
        file.save(app.config['UPLOAD_FOLDER']+filename)
#        split('full_image.png')
        redirect(url_for('uploaded_file',filename=filename))
        identification()
        redirect(url_for('uploaded_file', filename='ouput_image.png'))
        img_str = base64.b64encode(open(app.config['UPLOAD_FOLDER']+'ouput_image.png', "rb").read())
        response = make_response(img_str)
#        response = redirect(url_for('uploaded_file',filename=filename))
        response.headers.set('Content-Type', 'image/jpeg')
        return response
    return 'test'

#@app.route('/post/idf', methods=['POST'])
#def image_idf():
#    if os.path.exists('images/full_image.png'):
#        identification()
#        return redirect(url_for('uploaded_file', filename='ouput_image.png'))
#    else:
#        return 'full_image not exists'
    
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
    
#with open('result.png', 'rb') as file_xlsx:
#    files = {'file': file_xlsx}
#    res = requests.post("https://hello-egg-cookie.herokuapp.com/post/ticket", files=files)