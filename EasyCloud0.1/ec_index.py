from flask import Flask
from flask import render_template,make_response,send_from_directory
from flask import request,session,redirect,url_for
from werkzeug import secure_filename

from ec_config import config as cfg
from ec_utils import *
from ec_verify import verify
from ec_time import Timer

from threading import Thread
from gevent import pywsgi
app = Flask(__name__)

iplist = []

@app.route("/",methods=['GET','POST'])
def HTML_verify():
    ''' verify target user'''

    if request.method == 'GET':
        _ip = request.remote_addr
        if _ip in iplist:
            return redirect(url_for('HTML_entry'))
        else:
            return render_template("verify.html")
    elif request.method == 'POST':
        _password = request.form["password"]
        if verify(_password):
            iplist.append(request.remote_addr)
            return "success"
        else:
            return "failed"


@app.route("/entry")
def HMTL_entry():

    if request.remote_addr in iplist:
        return render_template("index.html",config=cfg)
    return redirect(url_for('HTML_verify'))

@app.route("/hello")
def HTML_hello():

    if request.remote_addr in iplist:
        return render_template("hello.html",config=cfg)
    return redirect(url_for("HTML_verify"))

@app.route("/filelist/<path:pathname>")
def HTML_files(pathname):

    if request.remote_addr in iplist:
        _pathname = pathname + "/"
        files = scan_floder_first(_pathname)
        return render_template("filelist.html",config=cfg,files=files,current_path=pathname)
    else:
        return redirect(url_for("HTML_verify"))

@app.route('/download/<path:path_name>')
def download(path_name):

    if request.remote_addr in iplist:
        directory = os.path.dirname(path_name)
        filename = path_name.split("/")[-1]
        res = make_response(send_from_directory(directory,filename,as_attachment=True))
        return res
    else:
        return redirect(url_for("HTML_verify"))

@app.route("/upload/<path:path_name>",methods=['POST'])
def upload_file(path_name):
    '''upload a new file in current floder'''

    if request.remote_addr in iplist:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = secure_filename(file.filename)
                if os.path.exists(path_name):
                    return "upload failed"
                else:
                    file.save(path_name)
                    return "upload success"
    else:
        return redirect(url_for("HTML_verify"))

@app.route("/remove",methods=['POST'])
def remove_files():
    '''remove target file in current floder'''

    if request.remote_addr in iplist:
        if request.method == 'POST':
            files = eval(request.form.get("files_json_value"))
            try:
                for file in files:
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
    else:
        return redirect(url_for("HTML_verify"))

@app.route("/folder/<path:path_name>",methods=['POST'])
def create_folder(path_name):
    ''' create a new folder in current folder'''

    if request.remote_addr in iplist:
        if request.method == 'POST':
            _folder_name = request.form.get("folder_name")
            if _folder_name:
                os.mkdir(os.path.join(path_name,_folder_name))
                return "create success"
    else:
        return redirect(url_for("HTML_verify"))



_timer = Timer(24 * 3600)
def _clear(_timer,iplist):

    print("ip刷新器开启")
    while 1:
        if _timer.tick():
            iplist.clear()

t = Thread(target=_clear,args=(_timer,iplist))
t.start()

if __name__ == '__main__':

    # app.run(host="127.0.0.1",threaded=True,port=45534)
    # t.start()
    gserver = pywsgi.WSGIServer(('0.0.0.0',45534),app)
    gserver.serve_forever()
    