from distutils.core import setup


if __name__ == '__main__':
      setup(name='Password_Manager',
            version='0.5',
            description='Python password-manager with GUI',
            author='Frederik Andersen',
            author_email='frederik.andersen@fau.de',
            url='https://github.com/AndersenFred/password_manager',
            packages=['numpy', 'PyQt6', 'getpass', 'json', 'hashlib', 'PyCryptodome', 'clipboard', 'base64'],
            )
