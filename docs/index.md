---
layout: default
title: Home
nav_order: 1
---

# Teflo Notify Service Plugin
{: .no_toc }

This is Teflo's plugin for sending teflo notifications using Notify Service. Notify service is a 
backend service build with FastAPI that supports sending notifications to multiple supported targets
(gchat, slack, unified message bus, email and irc)
To learn more about the notify service please visit [here](https://github.com/waynesun09/notify-service)

This plugin is used to send notifications on triggers like `on_task`, `on_start`, `on_failure`, `on_demand`
during and post teflo execution. For more information on how to setup triggers for notification
please visit [here](https://teflo.readthedocs.io/en/latest/users/definitions/notifications.html#triggers).

To know more about teflo please visit [here](https://teflo.readthedocs.io/en/latest/).
