from flask import Flask
from flask import render_template,make_response,send_from_directory
from flask import request
from werkzeug import secure_filename

from ec_config import config as cfg
from ec_utils import *
app = Flask(__name__)


@app.route("/")
def HMTL_entry():

    return render_template("index.html",config=cfg)

@app.route("/hello")
def HTML_hello():

    return render_template("hello.html",config=cfg)

@app.route("/filelist/<path:pathname>")
def HTML_files(pathname):

    _pathname = pathname + "/"
    files = scan_floder_first(_pathname)
    return render_template("filelist.html",config=cfg,files=files,current_path=pathname)

@app.route('/download/<path:path_name>')
def download(path_name):

    directory = os.path.dirname(path_name)
    filename = path_name.split("/")[-1]
    res = make_response(send_from_directory(directory,filename,as_attachment=True))
    return res

@app.route("/upload/<path:path_name>",methods=['POST'])
def upload_file(path_name):
    '''upload a new file in current floder'''

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            if os.path.exists(path_name):
                return "upload failed"
            else:
                file.save(path_name)
                return "upload success"

@app.route("/remove",methods=['POST'])
def remove_files():
    '''remove target file in current floder'''

    if request.method == 'POST':
        files = eval(request.form.get("files_json_value"))
        try:
            for file in files:
                print(file)
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    delete_folder(file)

            if not os.path.exists("./Files"):
                os.mkdir("./Files")
            return "delete success"
        except FileNotFoundError as e:
            print(e)
            return "delete failed"

@app.route("/folder/<path:path_name>",methods=['POST'])
def create_folder(path_name):
    ''' create a new folder in current folder'''

    if request.method == 'POST':
        _folder_name = request.form.get("folder_name")
        if _folder_name:
            os.mkdir(os.path.join(path_name,_folder_name))
            return "create success"

if __name__ == '__main__':

    app.run(host="127.0.0.1",port=45534,debug=True)
