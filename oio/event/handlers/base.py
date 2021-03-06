# Copyright (C) 2015-2019 OpenIO SAS, as part of OpenIO SDS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from oio.event.consumer import StopServe
from oio.event.evob import Event, EventOk, EventError


class Handler(object):
    def __init__(self, app, conf):
        self.app = app
        self.app_env = app.app_env
        self.conf = conf
        self.logger = app.logger

    def process(self, event):
        return EventOk(event=event)

    def __call__(self, env, beanstalkd, cb):
        event = Event(env)
        try:
            res = self.process(event)
            return res(env, beanstalkd, cb)
        except StopServe:
            self.logger.info('Job %s not handled: the process is stopping',
                             event.job_id)
            res = EventError(event=event, body='Process is stopping')
        except Exception as err:
            self.logger.exception('Job %s not handled: %s', event.job_id, err)
            res = EventError(event=event, body='An error ocurred')
        return res(env, beanstalkd, cb)


def handler_factory(app, global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    handler = Handler(app, conf)
    return handler
