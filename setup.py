from setuptools import setup, find_packages

print find_packages()

desc = '''can be used where all django projects are deployed in the same manner
and is necessary to process a setting file which reside in the same place
within each django project root.
'''

setup(
    name='django-projectgroup-settings-iterator',
    version='0.1',
    description=desc,
    author='Vaclav Klecanda',
    author_email='vencax77@gmail.com',
    url='https://github.com/vencax/django-mailserver',
    packages=find_packages()
)
