# User Guide

### To return to documentation home page press [here](https://redhatqe.github.io/teflo_notify_service_plugin/index.html).

## Installation

### Before Install
In order to use this plugin, user has to setup notify service. Please visit [here](https://github.com/waynesun09/notify-service)
to get more inforation. 
User will also need teflo installed

**Note** 

This plugin is supported only with Python 3

### Install
To install the plugin you can use pip. 

```bash
$ pip install teflo_notify_service_plugin==<tagged_version>
```

OR

```bash
$ pip install https://github.com/RedHatQE/teflo_notify_service_plugin.git@<tagged_version>
```

## Credentials
In teflo.cfg, users will need to provide following information under the credential section as below:

```ini
[credentials:notify_service]
gchat_url=<gchat webhook url>
slack_url=<slack webhook url>
service_api=<notify service api>
token=<unique token to access the service api>

```

**Note**

gchat_url/slack_url are required when sending notifications to ghcta/slack

Please read [here](https://github.com/waynesun09/notify-service#update-helm-chart-value) to understand how to get a 
unique token

## Notification block under Teflo SDF
Within teflo scenario descriptor file (SDF) following attributes that can be set for
notification block for notify_service 

```yaml
notifications:
  - name: test_notify_service
    notifier: notify_service
    credential: notify_service
    params:
      target: 'gchat,email,slack,irc,message_bus'
      subject: Notification on demand
      irc_channel: '#ccit'
      gchat_template_name: teflo_scenario_gchat
      email_template_name: teflo_scenario_email
      email_template_url: https://raw.githubusercontent.com/waynesun09/notify-service/main/app/templates/build/teflo_scenario_email.html
      email_to: ['rushinde@redhat.com']
      message_bus_topic: "/topic/VirtualTopic.qe.ci.qedevops_teflo.brew-build.test.complete"
      message_bus_request_body: {'body': 'text1'}
      message_body: {"body": { "scenario":  {"name": "notify_service_all", "overall_status": 0},"passed_tasks": ["validate", "provision", "orchestrate"]}}
      .
      .
      .  

```

<table class="tg">
  <tr>
    <th class="tg-7un6">Key</th>
    <th class="tg-14gg">Description</th>
    <th class="tg-14gg">Type/Value</th>
    <th class="tg-14gg">Required</th>
  </tr>
  <tr>
    <td class="tg-8m83">name</td>
    <td class="tg-8m83">name for the notification block<br><span style="font-style:italic">  </span></td>
    <td class="tg-8m83">String</td>
    <td class="tg-8m83">True</td>
  </tr>
  <tr>
    <td class="tg-14gg">notifier</td>
    <td class="tg-14gg">Plugin name</td>
    <td class="tg-14gg">notifier_service</td>
    <td class="tg-14gg">True</td>
  </tr>
  <tr>
    <td class="tg-8m83">credential</td>
    <td class="tg-8m83"> credential name in teflo.cfg </td>
    <td class="tg-8m83">String</td>
    <td class="tg-8m83">True</td>
  </tr>
  <tr>
    <td class="tg-14gg">params</td>
    <td class="tg-14gg">A dictionary of parameters used by the notify service</span> key</td>
    <td class="tg-14gg">Dictionary</td>
    <td class="tg-14gg">True</td>
  </tr>
  </table>
  
  
  Following table shows the different parameters the **params** key takes
  
  <table class="tg">
   <tr>
    <th class="tg-7un6">Key</th>
    <th class="tg-14gg">Description</th>
    <th class="tg-14gg">Type/Value</th>
    <th class="tg-14gg">Required</th>
    <th class="tg-14gg">Notes</th>
  </tr>
   <tr>
    <td class="tg-14gg">target</td>
    <td class="tg-14gg">A comma separated string of targets</td>
    <td class="tg-14gg">String </td>
    <td class="tg-14gg">True</td>
    <td class="tg-14gg"> Valid values : gchat,slack,email,message_bus,irc. Atleast one target value is required</td>
  </tr>
  <tr>
    <td class="tg-14gg">subject</td>
    <td class="tg-14gg">Subject of the notification</span> </td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">True</td>
    <td class="tg-14gg"> - </td>
  </tr>
  <tr>
    <td class="tg-14gg">irc_channel</td>
    <td class="tg-14gg">IRC channel name start with '#' or a user name</td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">True when irc is mentioned under target</td>
    <td class="tg-14gg"> - </td>
  </tr>
  <tr>
    <td class="tg-14gg">gchat_template_url</td>
    <td class="tg-14gg">gchat remote template raw url</span> </td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> This needs to be the raw url </td>
  </tr>
  <tr>
    <td class="tg-14gg">gchat_template_name</td>
    <td class="tg-14gg">name of the template present on the notify_service server</td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> If template_url is provided it precedes over the template name. If both template url and name are not provided teflo_scenario_gchat template is used  as default</td>
  </tr>
  <tr>
    <td class="tg-14gg">slack_template_url</td>
    <td class="tg-14gg">slack remote template raw url</span> </td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> This needs to be the raw url</td>
  </tr>
  <tr>
    <td class="tg-14gg">slack_template_name</td>
    <td class="tg-14gg">name of the template present on the notify_service server</span> </td>
    <td class="tg-14gg">String </td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> If template_url is provided it precedes over the template name. If both template url and name are not provided teflo_scenario_slack template is used as default </td>
  </tr>
  <tr>
    <td class="tg-14gg">email_template_url</td>
    <td class="tg-14gg">email remote template raw url</span> </td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> This needs to be the raw url</td>
  </tr>
  <tr>
    <td class="tg-14gg">email_template_name</td>
    <td class="tg-14gg">name of the template present on the notify_service server</span> </td>
    <td class="tg-14gg">String </td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> If template_url is provided it precedes over the template name. If both template url and name are not provided teflo_scenario_slack template is used as default </td>
  </tr>
  <tr>
    <td class="tg-14gg">email_to</td>
    <td class="tg-14gg">A comma separated string of targets</span> </td>
    <td class="tg-14gg">String Valid values : gchat,slack,email,message_bus,irc</td>
    <td class="tg-14gg">True if email is in the target</td>
    <td class="tg-14gg"> - </td>
  </tr>  
  <tr>
    <td class="tg-14gg">message_bus_topic</td>
    <td class="tg-14gg">Topic to be sent on teh UBM</span> </td>
    <td class="tg-14gg">String</td>
    <td class="tg-14gg">True if message_bus is in the target</td>
    <td class="tg-14gg"> - </td>
  </tr>
  <tr>
    <td class="tg-14gg">message_bus_request_body</td>
    <td class="tg-14gg">A comma separated string of targets</span> </td>
    <td class="tg-14gg">String Valid values : gchat,slack,email,message_bus,irc</td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> If provided a separet api call is made to send notification to the UMB. 
    If not provided a single api call is made with all the targets included</td>
  </tr>
    <tr>
    <td class="tg-14gg">message_body</td>
    <td class="tg-14gg">Body of the message to be sent</span> </td>
    <td class="tg-14gg">String/Dict</td>
    <td class="tg-14gg">False</td>
    <td class="tg-14gg"> If not provided a default message body is used</td>
  </tr>
  </table>
   
  **Note**
  Following are some notes to keep in mind before putting together the notifictaion block for notify_service
  1. The template_url for gchat/slack/email need to be in raw format. The template stored on github/gitlab can give you the 
     raw url, if you open up the template as openraw on gitlab and raw on github and then copy the url from the browser.
  2. template url has higher precedence than the template_name
  3. When providing template_name , you need to make sure the template exist on the notify_service, else it will throw an error
     Please visit [here](https://github.com/waynesun09/notify-service#templates) to get more information on how to set up templates
  4. When sending notification to UMB, if a message_request_body is provided in the SDF, a separate api clal is made, else
     notifications are sent to all targets including UMB in a signle api call. This is because notify_service cannot verify
     different combinations of the request body can have
        

## Examples

For all the examples the credentials need to be set in the teflo.cfg
 ```ini
[credentials:notify_service]
gchat_url=<gchat webhook url set when sending message to gchat>
slack_url=<slack webhook url set when sending message to slack>
service_api=<notify service api>
token=<unique token to access the service api>
```

### Example 1

To send notification to slack,gchat,email,irc, message_bus without the message_bus_request_body on completion of the 
teflo execute task

Here notification with subject 'Notification using notify service' is sent to the following after execute 
task completes (here one single api call is made to send notification to all the targets)
1. **gchat** using the template teflo_scenario_gchat template
2. **slack** using the template teflo_scenario_slack template
3. **email** using the raw template url provided
4. **irc** to #ccit channel
5. **message bus** with topic "/topic/VirtualTopic.qe.ci.qedevops_teflo.brew-build.test.complete" and no request body

```yaml
notifications:
  - name: notify1
    notifier: notify_service
    credential: notify_service
    on_task: ['execute']
    params:
      target: 'gchat,email,slack,irc,message_bus'
      subject: Notification using notify service
      irc_channel: '#ccit'
      gchat_template_name: teflo_scenario_gchat
      slack_template_name: teflo_scenario_slack
      email_template_name: teflo_scenario_email
      email_template_url: https://raw.githubusercontent.com/waynesun09/notify-service/main/app/templates/build/teflo_scenario_email.html
      email_to: ['abcd@redhat.com']
      message_bus_topic: "/topic/VirtualTopic.qe.ci.qedevops_teflo.brew-build.test.complete"
      message_body: {"body": { "scenario":  {"name": "notify_service_all", "overall_status": 0},"passed_tasks": ["validate", "provision", "orchestrate"]}}
    
```  


### Example 2

To send notification to slack,gchat,email,irc, message_bus with the message_bus_request_body on failure of the
teflo report task

Here two separate api calls are made to teh notify service one for message_bus and one for all other targets.

```yaml
notifications:
  - name: notify2
    notifier: notify_service
    credential: notify_service
    on_task: ['execute']
    params:
      target: 'gchat,email,slack,irc,message_bus'
      subject: Notification using notify service
      irc_channel: '#ccit'
      gchat_template_name: teflo_scenario_gchat
      slack_template_name: teflo_scenario_slack
      email_template_name: teflo_scenario_email
      email_template_url: https://raw.githubusercontent.com/waynesun09/notify-service/main/app/templates/build/teflo_scenario_email.html
      email_to: ['abcd@redhat.com']
      message_bus_topic: "/topic/VirtualTopic.qe.ci.qedevops_teflo.brew-build.test.complete"
      message_body: {"body": { "scenario":  {"name": "notify_service_all", "overall_status": 0},"passed_tasks": ["validate", "provision", "orchestrate"]}}
      message_bus_request_body: {
  "headers": {
    "CI_NAME": "EXAMPLE",
    "CI_TYPE": "CUSTOM"
  },
  "body": {
    "contact": {
      "name": "C3I Jenkins",
      "team": "DevOps_rujuta",
      "url": "https://example.com",
      "docs": "https://example.com/user-documentation",
      "irc": "#some-channel",
      "email": "someone@example.com"
    },
    "run": {
      "url": "https://somewhere.com/job/ci-job/4794",
      "log": "https://somewhere.com/job/ci-job/4794/console",
      "log_raw": "https://somewhere.com/job/ci-job/4794/consoleText",
      "log_stream": "https://somewhere.com/job/ci-job/4794/consoleText",
      "debug": "https://somewhere.com/job/ci-job/4794/artifacts/debug.txt",
      "rebuild": "https://somewhere.com/job/ci-job/4794/rebuild/parametrized"
    },
    "artifact": {
      "type": "container-image",
      "repository": "someapp",
      "digest": "sha256:017eb7de7927da933a04a6c1ff59da0c41dcea194aaa6b5dd7148df286b92433",
      "pull_ref": "docker://registry.fedoraproject.org/someapp@sha256:017eb7de7927da933a04a6c1ff59da0c41dcea194aaa6b5dd7148df286b92433",
      "source": "git+https://src.fedoraproject.org/rpms/setup.git?#5e0ae23a",
      "id": "someapp@sha256:017eb7de7927da933a04a6c1ff59da0c41dcea194aaa6b5dd7148df286b92433"
    },
    "pipeline": {
      "id": "ac11dcddf99a",
      "name": "ci-job"
    },
    "test": {
      "type": "tier1",
      "category": "functional",
      "result": "failed",
      "namespace": "factory2.c3i-ci",
      "note": "Some notes.",
      "label": [
        "fast",
        "aarch64"
      ],
      "xunit": "https://somewhere.com/job/ci-openstack/4794/artifacts/results.xml"
    },
    "system": [
      {
        "os": "docker.io/openshift/jenkins-slave-base-centos7:latest",
        "provider": "openshift",
        "architecture": "x86_64"
      }
    ],
    "notification": {
      "recipients": [
        "ovasik",
        "mvadkert"
      ]
    },
    "generated_at": "2018-05-10 08:58:31.222602",
    "version": "0.2.1"
  }
}

```


### Example 3

To send notification email,irc on start of all teflo tasks

This notifictaion will be sent to email and irc channel at the beginning of every teflo task


```yaml
notifications:
  - name: notify3
    notifier: notify_service
    credential: notify_service
    on_start: True
    params:
      target: 'email,irc'
      subject: Notification using notify service
      irc_channel: '#ccit'
      email_template_url: https://raw.githubusercontent.com/waynesun09/notify-service/main/app/templates/build/teflo_scenario_email.html
      email_to: ['abcd@redhat.com']
```  


### Example 4

To send notification on demand, run the notify command post the teflo run has completed providing the results.yml 
as the scenario file or can run it anytime using the original SDF

```bash
teflo notify -s .teflo/.results/results.yml 

or 

teflo notify -s scenario.yml

```

```yaml
notifications:
  - name: notify4
    notifier: notify_service
    credential: notify_service
    on_demand: True
    params:
      target: 'email,irc,gchat'
      subject: Notification using notify service
      gchat_template_name: teflo_scenario_gchat
      irc_channel: '#ccit'
      email_template_url: https://raw.githubusercontent.com/waynesun09/notify-service/main/app/templates/build/teflo_scenario_email.html
      email_to: ['abcd@redhat.com']
```    
