from distutils.log import debug
from flask import Flask
from flask_socketio import SocketIO,send
from flask_sqlalchemy import SQLAlchemy
from numpy import broadcast


app=Flask(__name__)
app.config['SECRET_KEY']='sisecret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
socket=SocketIO(app,cors_allowed_origins="*")



class Results(db.Model):
    

    id=db.Column('id',db.Integer,primary_key=True)
    vote=db.Column('vote',db.Integer)

@socket.on('vote')
def handleVote(ballot):
    vote=Results(vote=ballot)
    db.session.add(vote)
    db.session.commit()

    results1=Results.query.filter_by(vote=1).count()
    results2=Results.query.filter_by(vote=2).count()

    socket.emit('vote_results',{"results1":results1,"results2":results2},broadcast=True)

# @socket.on('message')
# def handleMessage(msg):
#     print(msg)
#     send(msg,broadcast=True)

# @socket.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))

if __name__=='__main__':
    socket.run(app,debug=True)