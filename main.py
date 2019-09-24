"""
@author: Guilherme Esgario
@email: guilherme.esgario@gmail.com
"""

import os
import json
import base64
from flask import Flask, request, render_template
from mlq.queue import MLQ
from werkzeug.utils import secure_filename

import worker

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'TytNr1_MxgNHlKjdW7GZ8w'
app.config['IN_IMAGES_PATH'] = 'in_images'
app.config['OUT_IMAGES_PATH'] = 'out_images'

# Create MLQ: namespace, redis host, redis port, redis db
mlq = MLQ('prediction_app', 'redis', 6379, 0)


'''
METHODS
'''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''
ENDPOINTS
'''
@app.route('/api/status/<job_id>', methods=['GET'])
def get_progress(job_id):
    """
        Get a json informing the status of the inference.
    """
    job_progress = mlq.get_progress(job_id)
    return json.dumps({'status': job_progress})

@app.route('/api/result/<job_id>', methods=['GET'])
def get_result(job_id):
    """
        Get a json with:
            - ['status'] image processing status (started or completed)
            - ['result'] algorithm return text
            - ['filename']
            - ['file'] base64 enconded image
    """
    job_progress = mlq.get_progress(job_id)
    
    try:
        job = mlq.get_job(job_id)
        ret = job['result']        
        response = {'status': job_progress}
        
        if ret is not None:
            # if there is a file in ret so...
            if 'file' in ret:
                with open(os.path.join(app.config['OUT_IMAGES_PATH'], ret['file']), "rb") as fp:
                    encoded_string = base64.b64encode(fp.read())
                    encoded_string = encoded_string.decode('ascii')
                    response = {'status': job_progress,
                                'result': ret['result'],
                                'filename': ret['file'],
                                'file': encoded_string }
                
            # otherwise
            else:
                response = {'status': job_progress,
                            'result': ret['result'],
                            'filename': ret['file']}
        
        return json.dumps(response)
        
    except:
        return json.dumps({'status': job_progress})
    


@app.route('/api/inference', methods=['POST'])
def do_inference():
    """
        Start inference and returns a json with ['job_id'] or an ['error_code'].
    """
    # check if the post request has the file part
    if 'file' not in request.files:
        return json.dumps({'error_code': 0, 'msg': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return json.dumps({'error_code': 1, 'msg': 'No file selected for uploading'})
    
    if file and allowed_file(file.filename):
#        file.filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['IN_IMAGES_PATH'], file.filename))                
        job_id = mlq.post({'algorithm':request.form['algorithm'], 'file':file.filename})
        return json.dumps({'job_id': job_id})
    else:    
        return json.dumps({'error_code': 2, 'msg': 'File extension not allowed'})

# ROOT
@app.route('/')
def index():
    return render_template("index.html");