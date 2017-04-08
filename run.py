from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def runapp(debug=False, initDb=False, port=8888):
    if initDb:
        print "Attempting to create all missing DB tables ..."
        db.create_all()
    return app.run(host='127.0.0.1', port=port, debug=debug, threaded=True)

if __name__ == "__main__":
    manager.run()
