'''
Created on May 9, 2012

@author: vencax
'''
import unittest
import os
import shutil
from .settings import Settings


class _DebugSettings(Settings):
    sett = {}
    settings_module_name = 'test_settings'

    def process_project_settins(self, proj_sett, proj_path):
        self.sett[proj_path] = proj_sett


class DjangoProjectRootTestCase(unittest.TestCase):

    settings_module_name = 'test_settings.py'

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.prepareEnv()

    def tearDown(self):
        shutil.rmtree(self._test_root)
        unittest.TestCase.tearDown(self)

    def prepareEnv(self):
        _proj_root = os.path.dirname(os.path.dirname(__file__))
        self._test_root = os.path.join(_proj_root, '_testTMP')

        if os.path.exists(self._test_root):
            shutil.rmtree(self._test_root)
        os.mkdir(self._test_root)

        testConfigFile = os.path.join(self._test_root, '_example_cfg.py')
        os.environ['DJANGO_PROJECTROOT_CONF_FILE'] = testConfigFile

        self.projects_root = os.path.join(self._test_root, 'test_project_root')
        os.mkdir(self.projects_root)

        self.path_to_settings = 'mysite/settings'
        self.path_to_python = 'virtenv/bin/python'
        self.path_to_manage = ''
        with open(testConfigFile, 'w') as f:
            f.write('PROJECTS_ROOT=\'%s\'\n' % self.projects_root)
            f.write('PATH_TO_SETTINGS=\'%s\'\n' % self.path_to_settings)
            f.write('PATH_TO_PYTHON=\'%s\'\n' % self.path_to_python)
            f.write('PATH_TO_MANAGE=\'%s\'\n' % self.path_to_manage)
            self.prepareConfigExtras(f)

        for p in self.testDomains:
            self._create_domain_fldr(p)

    def prepareConfigExtras(self, cfgfilestram):
        pass

    def _create_domain_fldr(self, domain):
        domFolder = os.path.join(self.projects_root, domain)
        os.mkdir(domFolder)
        settingsFolder = os.path.join(domFolder, self.path_to_settings)
        os.makedirs(settingsFolder)

        open(os.path.join(settingsFolder, '__init__.py'), 'w').close()
        with open(os.path.join(settingsFolder,
                               '%s.py' % self.settings_module_name), 'w') as f:
            cntnt = '''
SETTINGS = [
    ('%s', {
        'accountcallback': 'onAccountCallback',
        'whateverElse': 'onWhaeverElse'
    }, 'domainwide_forward@address.com')
]
'''
            f.write(cntnt % domain)


class TestProjectrootSetting(DjangoProjectRootTestCase):

    testDomains = ('example1.com', 'example2.com', 'sample2.net')

    def test_settings(self):
        s = _DebugSettings()
        s.load_config()

        desired = {}
        for d in self.testDomains:
            projPath = os.path.join(self.projects_root, d)
            sett = {'SETTINGS': [
                (d, {
                    'accountcallback': 'onAccountCallback',
                    'whateverElse': 'onWhaeverElse'
                }, 'domainwide_forward@address.com')
            ]}
            desired[projPath] = sett

        assert s.sett == desired, 'settings loaded incorrectly'


if __name__ == '__main__':
    unittest.main()
