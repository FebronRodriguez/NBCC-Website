import os
from flask import Flask, flash, request, redirect, url_for , render_template ,send_from_directory
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)

#MySQL DB Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MYSQL
mysql = MySQL(app)

#Root Directory Path
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Folder Configs
#UPLOAD_FOLDER = os.path.join(APP_ROOT,'pdfdata/HRM/Jobs')
JOBS_FOLDER =  os.path.join(APP_ROOT,'pdfdata/Jobs')

#Allowed Extentions for file uploads
ALLOWED_EXTENSIONS = set(['pdf'])


#Route to Home
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

#Route to About
@app.route('/aboutus')
def about():
    return render_template('aboutus.html')
    

#File Retrival
@app.route('/files/<filename>')
def mysql_show(filename):
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT filePath FROM file WHERE fileName = %s',[filename])
    if result > 0:
        data=cur.fetchone()
        
        cur.close()
        filepath = data['filePath']
        path = (str(os.path.join(APP_ROOT,filepath)))
        
        return send_from_directory(path,filename)
        
    else:
        return '404'   

if __name__ == '__main__':
    app.run(debug = True)