import random
import string
import uuid
import hashlib
import base64
import urllib.parse
from datetime import datetime
import time
import secrets

class UtilityGenerator:
    @staticmethod
    def generate_password(length=16, use_special=True):
        """Generate a secure random password"""
        characters = string.ascii_letters + string.digits
        if use_special:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each type
        password = []
        password.append(random.choice(string.ascii_uppercase))
        password.append(random.choice(string.ascii_lowercase))
        password.append(random.choice(string.digits))
        if use_special:
            password.append(random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill the rest
        for _ in range(length - len(password)):
            password.append(random.choice(characters))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def generate_username(style='standard', length=8):
        """Generate a random username"""
        adjectives = ['cool', 'happy', 'brave', 'mighty', 'swift', 'bright', 'clever', 'wild']
        nouns = ['tiger', 'eagle', 'dragon', 'wolf', 'phoenix', 'storm', 'thunder', 'shadow']
        numbers = ''.join(random.choices(string.digits, k=4))
        
        if style == 'standard':
            adj = random.choice(adjectives)
            noun = random.choice(nouns)
            return f"{adj}_{noun}_{numbers}"
        elif style == 'simple':
            return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        elif style == 'words':
            return f"{random.choice(adjectives)}{random.choice(nouns)}"
        else:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_uuid(version=4):
        """Generate UUID"""
        if version == 4:
            return str(uuid.uuid4())
        elif version == 1:
            return str(uuid.uuid1())
        elif version == 3:
            namespace = uuid.NAMESPACE_DNS
            name = str(time.time())
            return str(uuid.uuid3(namespace, name))
        else:
            return str(uuid.uuid4())

    @staticmethod
    def generate_random_number(min_val=1, max_val=100):
        """Generate random number"""
        return random.randint(min_val, max_val)

    @staticmethod
    def generate_random_string(length=16, include_special=True):
        """Generate random string"""
        characters = string.ascii_letters + string.digits
        if include_special:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return ''.join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def generate_hash(text, algorithm='sha256'):
        """Generate hash of text"""
        algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha224': hashlib.sha224,
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512,
            'blake2b': hashlib.blake2b,
            'blake2s': hashlib.blake2s
        }
        
        if algorithm not in algorithms:
            algorithm = 'sha256'
        
        hash_obj = algorithms[algorithm]()
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()

    @staticmethod
    def base64_encode(text):
        """Encode text to base64"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    @staticmethod
    def base64_decode(text):
        """Decode base64 to text"""
        try:
            return base64.b64decode(text.encode('utf-8')).decode('utf-8')
        except:
            return None

    @staticmethod
    def url_encode(text):
        """URL encode text"""
        return urllib.parse.quote(text, safe='')

    @staticmethod
    def url_decode(text):
        """URL decode text"""
        try:
            return urllib.parse.unquote(text)
        except:
            return None

    @staticmethod
    def timestamp_generator(format_type='unix'):
        """Generate timestamp"""
        current_time = time.time()
        
        if format_type == 'unix':
            return str(int(current_time))
        elif format_type == 'unix_ms':
            return str(int(current_time * 1000))
        elif format_type == 'iso':
            return datetime.fromtimestamp(current_time).isoformat()
        elif format_type == 'readable':
            return datetime.fromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")
        else:
            return str(int(current_time))

    @staticmethod
    def list_hash_algorithms():
        """List available hash algorithms"""
        return ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s']
