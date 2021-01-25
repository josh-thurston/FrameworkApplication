from flask import Flask
import os

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.urandom(24)


def main():
    configure()
    register_blueprints()
    app.run(debug=True)


def configure():
    register_blueprints()


def register_blueprints():
    from views import home_views, account_views, dashboard_views, vendors_views, product_views, framework_views, usr_admin_views
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(dashboard_views.blueprint)
    app.register_blueprint(vendors_views.blueprint)
    app.register_blueprint(product_views.blueprint)
    app.register_blueprint(framework_views.blueprint)
    app.register_blueprint(usr_admin_views.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
