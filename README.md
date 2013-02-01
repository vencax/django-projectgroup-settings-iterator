django-projectgroup-settings-iterator
=====================================

usefull where all django projects are deployed in the same manner
and is necessary to process a setting file which reside in the same
place within each django project root (i.e. mailserver_setting,
commands_setting, ...).

This is base for programs that do services for all the deployed django projects
and needs to run commands of this projects. Base class is a mixin class that you
can inherit.

All configs are stored in config module (/etc/django_projectroot_cfg.py
by default or can be overridden by DJANGO_MAILSERVER_CONF_FILE environment variable).
The config module can contain (othewise defauls are used) few definitions.
For detail see settings.py.
