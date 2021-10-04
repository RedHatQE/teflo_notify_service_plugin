# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Red Hat, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,d
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Teflo's notification plugin for notify_service.
    :copyright: (c) 2021 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""

# TODO future usecase : to put a template on the notify_service repo using the template put api, so teflo users
#  can put that repo once and use it agian for other runs > need to ask this

from teflo.helpers import template_render, schema_validator, generate_default_template_vars
from teflo.core import NotificationPlugin
from teflo.exceptions import TefloNotifierError
import os
import json
import urllib.parse
import http.client


class NotifyServicePlugin(NotificationPlugin):
    __plugin_name__ = 'notify_service'

    __schema_file_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__), "files/schema.yml"))
    __schema_ext_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                       "files/schema_extensions.py"))

    def __init__(self, notification):
        super(NotifyServicePlugin, self).__init__(notification=notification)

        self.scenario = getattr(self.notification, 'scenario')
        self.config_params = self.get_config_params()
        self.creds_params = self.get_credential_params()
        self.service_api = self.creds_params.get('service_api', None)
        self.gchat_url = self.creds_params.get('gchat_url', None)
        self.slack_url = self.creds_params.get('slack_url', None)
        self.token = self.creds_params.get('token', None)
        self.create_logger(name='teflo_notify_service_plugin', data_folder=self.config.get('DATA_FOLDER'))
        self.params = getattr(self.notification, 'params')
        self.body = getattr(self.notification, 'message_body', None)

    def check_for_template(self, template_name):
        """Method to call the api to make sure template with template_name exist on the notify_service repo"""
        api = "/api/v1/template/%s" % template_name
        if self.api_call('GET', api):
            return 1
        else:
            raise TefloNotifierError("Error finding template %s .error ")

    def get_params(self):
        # Create a dictionary with message_bus params and the rest of the target params, if message_request_body is
        # provided. Notify service cannot handle message_bus custom request body when using multi target api
        # When message_bus with custom request body is provided this notification is handled by separate api call.
        params = {}
        types = ['gchat', 'slack', 'email', 'irc', 'message_bus']
        ignore_keys = ['message_bus_request_body', 'target']
        if self.params and self.params.get('target'):
            target_val = self.params.get('target')
            list1 = target_val.lower().replace(' ', '').split(',')
            if False in [item in types and isinstance(item, str) for item in list1]:
                raise TefloNotifierError("Unknown target value %s found.Target should be one or more "
                                         "of this list: 'gchat,email,slack,irc,message_bus'" % target_val)

            if 'message_bus' in list1:
                # Creating message_bus params entry in case message_bus_request_body is provided
                if not self.params.get('message_bus_topic'):
                    raise TefloNotifierError("Message bus topic is required to be set in SDF to "
                                             "send notification via message bus")
                if self.params.get('message_bus_request_body'):
                    self.logger.debug("User has provided message_bus request body. Will send notification using "
                                      "separate api call")
                    params['message_bus'] = {'message_bus_topic': self.params.get('message_bus_topic'),
                                             'message_bus_request_body': self.params.get('message_bus_request_body')}
                    # removing message_bus as target so that multi_api call dosent consider it
                    list1.pop(list1.index('message_bus'))
                    ignore_keys.append('message_bus_topic')

            params['targets'] = {'target': ','.join(list1)}
            for key, value in self.params.items():
                if key not in ignore_keys:
                    params['targets'].update({key: value})

            return params
        else:
            raise TefloNotifierError("At least one Target(gchat/email/slack/irs/message_bus) are required to send "
                                     "notifications using the Notify Service")

    def generate_multi_api_string(self, params):

        api = "/api/v1/message_multi_targets/?"
        for item in ['gchat', 'slack', 'email']:
            if item in params['target']:
                # it first checks for template url, if not found looks for template name , and if that not provided
                # uses teflo_scenario_gchat as template
                temp_url = item + '_template_url'
                temp_name = item + '_template_name'
                default_temp = 'teflo_scenario_' + item
                if params.get(temp_url):
                    self.logger.debug("Template for %s is provided via url" % item)
                    continue
                elif params.get(temp_name) and \
                        self.check_for_template(params.get(temp_name)) == 1:
                    self.logger.debug("Using %s as the %s template" % (temp_name, item))
                    continue
                else:
                    # using default teflo gchat template if no gchat_template url or name is provided
                    params[temp_name] = default_temp

        if 'gchat' in params['target']:
            if not self.gchat_url:
                raise TefloNotifierError("gchat_url is not set under teflo.cfg")
            else:
                params['gchat_webhook_url'] = self.gchat_url

        if 'slack' in params['target']:
            if not self.slack_url:
                raise TefloNotifierError("slack_url is not set under teflo.cfg")
            else:
                params['slack_webhook_url'] = self.slack_url

        if 'email' in params['target']:
            if not params.get('email_to'):
                raise TefloNotifierError("email_to parameter is not set")

        encode = urllib.parse.urlencode(params, doseq=True, safe='', quote_via=urllib.parse.quote)
        api_url = api + encode

        return api_url

    def generate_multi_api_payload(self):
        if not self.body:
            # Create the message body in json format that will be used by the teflo templates in notify_service repo
            self.logger.info("No message body is provided. Teflo default message body and template will be used")
            temp_var = generate_default_template_vars(self.scenario, self.notification)
            data = dict()
            data.update({"body": {}})
            data['body']['scenario'] = dict()
            data['body']['scenario']['name'] = self.scenario.name
            data['body']['scenario']['overall_status'] = self.scenario.overall_status
            data['body']['passed_tasks'] = temp_var.get('passed_tasks')
            data['body']['failed_tasks'] = temp_var.get('failed_tasks')
            if self.scenario.get_executes():
                data['body']['scenario']['executes'] = list()
                for exe in self.scenario.get_executes():
                    exe_dict = dict()
                    exe_dict['name'] = exe.name
                    if exe.testrun_results:
                        exe_dict['testrun_results']['aggregate_testrun_results'][
                            'total_tests'] = exe.testrun_results.aggregate_testrun_results.total_tests
                        exe_dict['testrun_results']['aggregate_testrun_results'][
                            'passed_tests'] = exe.testrun_results.aggregate_testrun_results.passed_tests
                        exe_dict['testrun_results']['aggregate_testrun_results'][
                            'failed_tests'] = exe.testrun_results.aggregate_testrun_results.failed_tests
                        exe_dict['testrun_results']['aggregate_testrun_results'][
                            'skipped_tests'] = exe.testrun_results.aggregate_testrun_results.skipped_tests
                    data['body']['scenario']['executes'].append(exe_dict)
            if self.scenario.get_reports():
                data['body']['scenario']['reports'] = list()
                for rep in self.scenario.get_reports():
                    rep_dict = dict()
                    rep_dict['name'] = rep.name
                    rep_dict['importer_plugin_name'] = rep.importer_plugin_name
                    if rep.import_results:
                        if isinstance(rep.import_results, list):
                            rep_dict['import_results'] = list()
                            for res in rep.import_results:
                                rep_dict['import_results'].append({'testrun-url': res['testrun-url']})
                        else:
                            rep_dict['import_results'] = rep.import_results['dashboard_url']
                    data['body']['scenario']['reports'].append(rep_dict)
            self.logger.debug("Payload data when messgae body not provided is %s " % data)
            return json.dumps(data)
        else:
            # message body is provided
            self.logger.debug("Message body is provided by the user. This will be converted into json")
            if isinstance(self.body, str):
                self.body = str({'text': self.body})
            elif not isinstance(self.body, dict):
                raise TefloNotifierError("The body needs to be in a dictionary or string format %s " % self.body)
            return json.dumps(eval(str(self.body)))

    def api_call(self, op, api, payload=None):
        conn = http.client.HTTPSConnection(self.service_api)

        headers = {
            'content-type': "application/json",
            'X-API-KEY': self.token
        }
        try:
            conn.request(op, api, body=payload, headers=headers)
            res = conn.getresponse()
            data = res.read()
            if res.code == 200:
                self.logger.debug("Notification api call was successful with return code 200")
                return res.code
            else:
                raise TefloNotifierError("There was an error making the notification api call : %s " % data)
        except Exception as ex:
            raise TefloNotifierError("Error connecting to notify service %s" % ex)

    def notify_by_message_bus(self, message_bus_dict):
        api = "/api/v1/message_bus/?"
        encode = urllib.parse.urlencode({'topic': message_bus_dict['message_bus_topic']},
                                        safe='', quote_via=urllib.parse.quote)
        api_url = api + encode

        self.logger.info("User has provided request body which will be used as payload")
        if not isinstance(self.params.get('message_bus_request_body'), dict):
            raise TefloNotifierError("The message_bus_request_body needs to be in a dictionary format %s " %
                                     self.params.get('message_bus_request_body'))
        payload = json.dumps(eval(str(self.params.get('message_bus_request_body'))))

        if self.api_call("POST", api_url, payload):
            self.logger.info("Notification successful for message_bus ")

    def notify(self):
        """
        Implementation of the notify method for generating the
        notification and sending it to the notify service
        :return:
        """
        input_params = self.get_params()
        if input_params.get('message_bus'):
            self.logger.info("Sending notification to message bus")
            self.notify_by_message_bus(input_params.get('message_bus'))

        api = self.generate_multi_api_string(input_params.get('targets'))
        payload = self.generate_multi_api_payload()
        if self.api_call("POST", api, payload):
            self.logger.info("Notification successful for multi api ")

    def validate(self):

        schema_validator(schema_data=self.build_profile(self.notification),
                         schema_creds=self.creds_params,
                         schema_files=[self.__schema_file_path__],
                         schema_ext_files=[self.__schema_ext_path__])
