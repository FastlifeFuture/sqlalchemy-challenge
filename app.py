#Import Flask
from flask import Flask

#create an app and pass __name__
app = Flask(__name__)

#create variable for precipitation data
# Prcp = Prcp_df
#Develop the routes of the app

#Define the home page 
@app.route("/")
def home():
    print("Client request was recieved")
    """All availble api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br>")

# @app.route("/api/v1.0/precipitation")
# def home():
#     # print("Client request was recieved")

#     # return jsonify(Prcp)


if __name__ == "__main__":
    app.run(debug=True)