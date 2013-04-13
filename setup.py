from setuptools import setup


setup(
    name='django-potato-captcha',
    version='0.1',
    description='A very simple, clever Django captcha application',
    long_description=open('README.md').read(),
    author='Chris Van',
    author_email='cvan@mozilla.com',
    license='BSD',
    url='https://github.com/cvan/django-potato-captcha',
    packages=['django_potato_captcha',
              'django_potato_captcha/reporters'],
    install_requires=open('requirements.txt').read().strip().split(),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django'
    ]
)
