#encoding: utf-8

import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('default')
manager = Manager(app)


# 绑定app, db
migrate = Migrate(app, db)

# 添加MigrateCommand到manager中
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
