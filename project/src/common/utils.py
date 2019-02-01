from passlib.hash import pbkdf2_sha512
import re

class Utils(object):

    @staticmethod
    def email_is_valid(email):
        '''
        Checks if email entered follows the correct RegEx pattern
        :param email: (str) entered by user in login/signup
        :return: True if email matches pattern, False otherwise
        '''
        email_address_matcher = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        '''
        Hashes password using pbkdf2_sha512
        :param password: sha512 password from login/register form
        :return: A sha512 --> pbkdf2_sha512 encrypted password
        '''
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        '''
        Checks the password the user sent matches that of the database.
        The database password is encrypted more than user's password at this stage
        :param password: sha512-hashed password
        :param hashed_password:  pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        '''
        return pbkdf2_sha512.verify(password, hashed_password)
