import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='emailAuto',
    version='v2.2.2',
    packages=setuptools.find_packages(),
    url='https://github.com/Oxke/emailAuttachments',
    license='GNU GPLv3.0',
    author='Oxke',
    author_email='oseaetobia@gmail.com',
    description='Un progetto per selezionare e ordinare alcune mail ricevute',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['pyzmail36', 'imapclient', 'pycriptodome', 'keyring'],
    python_requires='~=3.6'
)
