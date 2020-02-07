from setuptools import setup, find_packages

setup(name='mgen',
      version='0.1',
      description='Generate randomized musical compositions based on probabilities.',
      url='https://github.com/Avantol13/mgen',
      author='Alexander VanTol',
      author_email='avantol13 at gmail dot com',
      license='GNU GENERAL PUBLIC LICENSE V3',
      packages=find_packages(),
      keywords="music generator theory probability random song melody tune",
      include_package_data=True,
      install_requires=[
            "mock==4.0.1",
      ]
      )
