from setuptools import setup, find_packages

setup(
    name='hopaas_client',
    version='0.0',
    packages=find_packages(),
    url='https://github.com/landerli/hopaas_client',
    license='MIT',
    author='Lucio Anderlini',
    author_email='lucio.anderlini@fi.infn.it',
    description='Hyperparameter Optimization as a Service (Client)',
    install_requires=[
        'numpy',
        'pytest',
        'requests'
    ]
)
