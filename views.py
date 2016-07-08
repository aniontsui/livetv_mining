# -*- coding: UTF-8 -*-
from markdown import markdown
from flask import render_template, request, current_app

from .forms import SearchRoomForm
from . import crawler
from .models import LiveTVSite, LiveTVChannel, LiveTVRoom, LiveTVHost

import codecs
import os


@crawler.route('/')
def index():
    """ 直播网站列表 """
    sites = []
    for site in LiveTVSite.query.filter_by(valid=True).order_by(LiveTVSite.order_int.asc()):
        site.roomtop = site.rooms.filter_by(openstatus=True).order_by(LiveTVRoom.spectators.desc())
        site.channeltop = site.channels.filter_by(valid=True).order_by(LiveTVChannel.room_total.desc(), LiveTVChannel.room_range.desc())
        sites.append(site)
    return render_template('crawler/index.html', sites=sites)


@crawler.route('/site/<int:site_id>')
def site(site_id):
    """ 网站详细&频道列表 """
    site = LiveTVSite.query.get_or_404(site_id)
    channels = site.channels.filter_by(valid=True).order_by(LiveTVChannel.room_total.desc(), LiveTVChannel.room_range.desc())
    return render_template('crawler/site.html', channels=channels, site=site)


@crawler.route('/channel/<int:channel_id>')
def channel(channel_id):
    """ 频道详细&房间列表 """
    channel = LiveTVChannel.query.get_or_404(channel_id)
    page = request.args.get('page', 1, type=int)
    pagination = channel.rooms.filter_by(openstatus=True) \
                        .order_by(LiveTVRoom.spectators.desc()).paginate(
                    page=page, error_out=False,
                    per_page=current_app.config['FLASK_ROOMS_PER_PAGE'])
    rooms = pagination.items
    return render_template('crawler/channel.html', channel=channel, rooms=rooms, pagination=pagination)


@crawler.route('/room/<int:room_id>')
def room(room_id):
    """ 房间详细 """
    room = LiveTVRoom.query.get_or_404(room_id)
    return render_template('crawler/room.html', room=room)


@crawler.route('/search', methods=['GET', 'POST'])
def search():
    """ 导航栏搜索 """
    form = SearchRoomForm()
    form.site_code.choices = [(site.code, site.name) for site in LiveTVSite.query.filter_by(valid=True).order_by(LiveTVSite.order_int.asc())]
    if form.validate_on_submit():
        pagination = LiveTVRoom.query.order_by(LiveTVRoom.spectators.desc())
        if form.room_name.data:
            pagination = pagination.filter(LiveTVRoom.name.like('%{}%'.format(form.room_name.data)))
        if form.only_opened.data:
            pagination = pagination.filter_by(openstatus=form.only_opened.data)
        if form.site_code.data:
            site_id_list = [site.id for site in list(LiveTVSite.query.filter_by(code=form.site_code.data))]
            pagination = pagination.filter(LiveTVRoom.site_id.in_(site_id_list))
        if form.host_nickname.data:
            host_id_list = [host.id for host in list(LiveTVHost.query.filter(LiveTVHost.nickname.like('%{}%'.format(form.host_nickname.data))))]
            pagination = pagination.filter(LiveTVRoom.host_id.in_(host_id_list))
        pagination = pagination.paginate(page=1, error_out=False,
                                         per_page=current_app.config['FLASK_SEARCH_PER_PAGE'] + 1)
        rooms = pagination.items
        return render_template('crawler/search.html', rooms=rooms, form=form,
                               over_query_count=len(rooms) > current_app.config['FLASK_SEARCH_PER_PAGE'])
    return render_template('crawler/search.html', form=form, rooms=[], over_query_count=False)


@crawler.route('/about')
def about():
    """ 关于 """
    with codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as mdf:
        mdhtml = markdown(mdf.read())
    return render_template('crawler/about.html', mdhtml=mdhtml)
