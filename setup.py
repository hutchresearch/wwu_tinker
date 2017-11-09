from setuptools import setup

setup(name='tinker',
      version='0.1.0a1',
      description='Free hyperparameter optimization webservice',
      url='http://github.com/hutchresearch/tinker',
      author='WWU',
      author_email='brian.hutchinson@wwu.edu',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
      ],
      packages=['tinker'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
