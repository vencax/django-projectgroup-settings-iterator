'''
Created on May 22, 2012

@author: vencax
'''
import os
import logging
import sys


class Settings(object):
    """
    Loads all setting folder.
    """

    def load_config(self):
        if 'DJANGO_PROJECTROOT_CONF_FILE' in os.environ:
            configfile = os.environ['DJANGO_PROJECTROOT_CONF_FILE']
        else:
            configfile = '/etc/django_projectroot_cfg.py'

        cfgPath = os.path.dirname(configfile)
        cfgModName = os.path.basename(configfile).rstrip('.py')
        sys.path.insert(0, cfgPath)

        cfgMod = __import__(cfgModName)

        self.projects_root = getattr(cfgMod, 'PROJECTS_ROOT', '/home')
        if not os.path.exists(self.projects_root):
            raise Exception('PROJECTS_ROOT %s not exists' % self.projects_root)

        self.path_to_settings = getattr(cfgMod, 'PATH_TO_SETTINGS',
                                       'mysite/settings')
        self.path_to_python = getattr(cfgMod, 'PATH_TO_PYTHON', 'virtenv/bin')
        self.path_to_manage = getattr(cfgMod, 'PATH_TO_MANAGE', 'mysite')

        self.process_specific_settings(cfgMod)

        self.reload_config()

    def process_specific_settings(self, cfgMod):
        pass

    def process_project_settins(self, proj_sett, proj_path):
        raise NotImplementedError('This shall be implemented in subclass')

    def reload_config(self):
        self.settings = {}
        for project in os.listdir(self.projects_root):
            projPath = os.path.join(self.projects_root, project)
            if not os.path.isdir(projPath) or project.startswith('.'):
                continue

            settingsFldr = os.path.join(projPath, self.path_to_settings)
            try:
                proj_sett = self._load_project_module(settingsFldr)
                self.process_project_settins(proj_sett, projPath)
            except ImportError:
                logging.debug('no %s in %s' % \
                    (self.settings_module_name, settingsFldr))
            except Exception, e:
                logging.exception(e)
        logging.debug('settings loaded ...')

    def _load_project_module(self, settingsFolder):
        sys.path.insert(0, settingsFolder)
        try:
            settings_mod = __import__(self.settings_module_name)
            reload(settings_mod)
            settings_dict = {}
            for k, v in settings_mod.__dict__.items():
                if k.isupper():
                    settings_dict[k] = v
            return settings_dict
        finally:
            sys.path.remove(settingsFolder)
