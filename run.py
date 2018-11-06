from modules.app import create_app
from database.db import DBHandler

app = create_app()


if __name__ == '__main__':
    handler = DBHandler(app.config['DATABASE_URL'])
    handler.create_tables()


    app.run(debug=True)

