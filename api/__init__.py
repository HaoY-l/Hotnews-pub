from flask import Blueprint
from .csdn import csdn_bp
from .ithome import ithome_bp
from .lol import lol_bp
from .v2ex import v2ex_bp
from .weibo import weibo_bp
from .refresh_all import refresh_bp
from .hotnews_all import hotnews_all_bp



def register_blueprints(app):
    # 在这里统一注册蓝图
    app.register_blueprint(ithome_bp)
    app.register_blueprint(lol_bp)
    app.register_blueprint(v2ex_bp)
    app.register_blueprint(weibo_bp)
    app.register_blueprint(refresh_bp)
    app.register_blueprint(hotnews_all_bp)