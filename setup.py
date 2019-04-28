import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='emAuttAchments',
    version='v3.0.2',
    packages=setuptools.find_packages(),
    url='https://github.com/Oxke/emailAuttachments',
    license='GNU GPLv3.0',
    author='Oxke',
    author_email='oseaetobia@gmail.com',
    description='Un progetto per selezionare e ordinare alcune mail ricevute',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['pyzmail36', 'imapclient', 'pycryptodome', 'keyring'],
    python_requires='~=3.6'
)
