from distutils.core import setup
setup(
  name='mailify',        
  packages=['mailify'],   # Chose the same as "name"
  package_dir={'': ''},
  version='v1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='Inlines css styles in html documents to make them usable in emails.',   # Give a short description about your library
  author='Darlington Onyemere', 
  author_email='anselem16m@gmail.com',     
  url='https://github.com/dino16m/mailify',   # Provide either the link to your github or to your website
  download_url='https://github.com/Dino16m/mailify/archive/v1.tar.gz',   
  keywords=['Styles', 'CSS', 'Email', 'Django'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'Django==3.0.7',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
