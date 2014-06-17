from setuptools import setup
setup(
    name='submittable_api_client',
    packages=['submittable_api_client'],
    version='0.6',
    license='MIT',
    description='A client wrapper for the Submittable.com API.',
    author='Shawn Rider',
    author_email='shawn@shawnrider.com',
    url='https://github.com/shawnr/submittable-api-client',
    download_url="""
        https://github.com/shawnr/submittable-api-client/archive/0.6.zip""",
    keywords=['API', 'REST', 'Submittable'],
    install_requires=['requests>=2.3.0'],
    classifiers=[],
)
