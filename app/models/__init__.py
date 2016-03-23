# -*- coding: UTF-8 -*-
from datetime import datetime
from selenium import webdriver

from .. import db


class LiveTVSite(db.Model):
    __tablename__ = 'livetvsite'
    ''' 直播网站 '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, doc='名称')
    displayname = db.Column(db.String(128), index=True, doc='显示名称')
    url = db.Column(db.String(1024), unique=True, index=True, doc='官网地址')
    scan_url = db.Column(db.String(256), index=True, doc='扫描链接')
    image_url = db.Column(db.String(1024), unique=True, index=True, doc='图片')
    since_date = db.Column(db.DateTime, default=datetime.utcnow, doc='新增时间')
    weight = db.Column(db.Integer, index=True, doc='权重')
    description = db.Column(db.String(1024), doc='描述')


class LiveTVChannel(object):
    ''' 频道 '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, doc='名称')
    url = db.Column(db.String(1024), unique=True, index=True, doc='官网地址')
    since_date = db.Column(db.DateTime, default=datetime.utcnow, doc='新增时间')
    last_scan_date = db.Column(db.DateTime, doc='最近一次扫描时间')
    site_id = db.Column(db.Integer, index=True, doc='关联官网')
    range = db.Column(db.Integer, default=0, doc='房间增减幅度')
    roomcount = db.Column(db.Integer, default=0, doc='活动房间总数')
    image_url = db.Column(db.String(1024), unique=True, index=True, doc='图片')

    @classmethod
    def scan_channel(cls):
        ''' 扫描频道 Override '''


class LiveTVRoom(object):
    WEIGHT_DISPLAYNAME = ''
    ''' 房间 '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, doc='名称')
    url = db.Column(db.String(512), unique=True, index=True, doc='访问URL')
    since_date = db.Column(db.DateTime, default=datetime.utcnow, doc='新增日期')
    popularity = db.Column(db.Integer, index=True, doc='人气')
    weight = db.Column(db.Integer, index=True, doc=WEIGHT_DISPLAYNAME)
    boardcaster = db.Column(db.String(128), index=True, doc='主播名')
    last_scan_date = db.Column(db.DateTime, doc='最近一次扫描时间')
    officeid = db.Column(db.String(128), index=True, doc='官方ID')
    follower = db.Column(db.Integer, index=True, doc='关注')

    @classmethod
    def scan_room(cls, site_url=None, channel_url=None):
        ''' 扫描房间 Override '''


def get_webdirver_client():
    return webdriver.Firefox()

from .douyu import DouyuTVChannel, DouyuTVRoom
from .zhanqi import ZhanqiTVChannel, ZhanqiTVRoom

LiveTVConfig = {
    'douyu': (DouyuTVChannel, DouyuTVRoom),
    'zhanqi': (ZhanqiTVChannel, ZhanqiTVRoom),
}


def get_instance_class(configname):
    ''' 根据配置返回对应类'''
    return LiveTVConfig.get(configname, None)
