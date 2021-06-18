# User Guide

### To return to documentation home page press [here](https://redhatqe.github.io/teflo_notify_service_plugin/index.html).

## Installation

### Before Install
In order to use this plugin, user has to setup notify service. Please visit [here](https://github.com/waynesun09/notify-service)
to get more inforation. 

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

```bash
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
    <td class="tg-14gg">A comma separated string of targets</span> </td>
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
    <td class="tg-14gg"> If template_url is provided it precedes over the template name. 
    If both template url and name are not provided teflo_scenario_gchat template is used </td>
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
    <td class="tg-14gg"> If template_url is provided it precedes over the template name. If both template url and name are not provided teflo_scenario_slack template is used </td>
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
    <td class="tg-14gg"> If template_url is provided it precedes over the template name. If both template url and name are not provided teflo_scenario_slack template is used </td>
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

### Example 1

To send notification to slack,gchat,email,irc, message_bus without the message_bus_request_body on completion of the 
teflo execute task

```yaml
notifications:
  - name: msg_template
    notifier: gchat-notifier
    credential: webhook
    on_task: ['provision']
    message_body: "Provsision task completed" 
```  


### Example 2

To send notification to slack,gchat,email,irc, message_bus with the message_bus_request_body on failure of the
teflo report task

```yaml
notifications:
  - name: msg_template
    notifier: gchat-notifier
    credential: webhook
    on_start: true
    message_template: user_template.txt
```


### Example 3

To send notification email,irc on start of all teflo tasks execute task


```yaml
notifications:
  - name: msg1
    notifier: gchat-notifier
    credential: webhook
    on_failure: true
```  


### Example 4

To send notification on demand

```yaml
notifications:
  - name: msg1
    notifier: webhook-notifier
    credential: webhook
    on_failure: true
    message_template: differnt_chat_app_template.jinja
```    

```
