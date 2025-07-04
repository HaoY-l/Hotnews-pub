from flask import Blueprint
from .kr36 import kr36_bp
from .cto51 import cto51_bp
from .pojie52 import pojie_bp
from .acfun import acfun_bp
from .baidu import baidu_bp
from .bilibili import bilibili_bp
from .csdn import csdn_bp
from .dgtle import dgtle_bp
from .douban_group import douban_group_bp
from .douban_movie import douban_movie_bp
from .douyin import douyin_bp
from .geekpark import geekpark_bp
from .github import github_bp
from .hackernews import hackernews_bp
from .hellogithub import hellogithub_bp
from .ifanr import ifanr_bp
from .ithome import ithome_bp
from .jianshu import jianshu_bp
from .lol import lol_bp
from .netease_news import netease_news_bp
from .newsmth import newsmth_bp
from .nytimes import nytimes_bp
from .qq_news import qqnews_bp
from .sina_news import sina_bp
from .sina import sina1_bp
from .smzdm import smzdm_bp
from .sspai import sspai_bp
from .thepaper import thepaper_bp
from .tieba import tieba_bp
from .toutiao import toutiao_bp
from .v2ex import v2ex_bp
from .weatheralarm import weather_bp
from .weibo import weibo_bp
from .weread import weread_bp
from .zhihu_daily import zhihu_daily_bp
from .zhihu import zhihu_bp
from .refresh_all import refresh_bp
from .hotnews_all import hotnews_all_bp


def register_blueprints(app):
    # 在这里统一注册蓝图
    app.register_blueprint(kr36_bp)
    app.register_blueprint(cto51_bp)
    app.register_blueprint(pojie_bp)
    app.register_blueprint(acfun_bp)
    app.register_blueprint(baidu_bp)
    app.register_blueprint(bilibili_bp)
    app.register_blueprint(csdn_bp)
    app.register_blueprint(dgtle_bp)
    app.register_blueprint(douban_group_bp)
    app.register_blueprint(douban_movie_bp)
    app.register_blueprint(douyin_bp)
    app.register_blueprint(geekpark_bp)
    app.register_blueprint(github_bp)
    app.register_blueprint(hackernews_bp)
    app.register_blueprint(hellogithub_bp)
    app.register_blueprint(ifanr_bp)
    app.register_blueprint(ithome_bp)
    app.register_blueprint(jianshu_bp)
    app.register_blueprint(lol_bp)
    app.register_blueprint(netease_news_bp)
    app.register_blueprint(newsmth_bp)
    app.register_blueprint(nytimes_bp)
    app.register_blueprint(qqnews_bp)
    app.register_blueprint(sina_bp)
    app.register_blueprint(sina1_bp)
    app.register_blueprint(smzdm_bp)
    app.register_blueprint(sspai_bp)
    app.register_blueprint(thepaper_bp)
    app.register_blueprint(tieba_bp)
    app.register_blueprint(toutiao_bp)
    app.register_blueprint(v2ex_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(weibo_bp)
    app.register_blueprint(weread_bp)
    app.register_blueprint(zhihu_daily_bp)
    app.register_blueprint(zhihu_bp)
    app.register_blueprint(refresh_bp)
    app.register_blueprint(hotnews_all_bp)