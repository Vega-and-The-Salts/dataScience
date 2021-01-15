import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
    
import pymysql
from flask_cors import CORS, cross_origin
from config import remote_db_endpoint, remote_db_port
from config import remote_db_name, remote_db_user, remote_db_pwd
pymysql.install_as_MySQLdb()
from sqlalchemy import func, create_engine

app = Flask(__name__)


engine = create_engine(f"mysql://{remote_db_user}:{remote_db_pwd}@{remote_db_endpoint}:{remote_db_port}/{remote_db_name}")

# create route that renders index.html template
@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/info")
def info():
    conn = engine.connect()
    
    query = f'''
        SELECT 
            *
        FROM
            geojsonLoc
    ''' 

    game_df = pd.read_sql(query, con=conn)
    game_json = game_df.to_json(orient='records')
    conn.close()

    return game_json

if __name__ == "__main__":
    app.run(debug=True)