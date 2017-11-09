from setuptools import setup

setup(name='wwu_tinker',
      version='0.1a1',
      description='Free hyperparameter optimization webservice',
      url='http://github.com/hutchresearch/wwu_tinker',
      author='WWU',
      author_email='brian.hutchinson@wwu.edu',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3',
      ],
      packages=['wwu_tinker'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
