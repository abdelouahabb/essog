# -*- coding: utf-8 -*-

# Copyright © 2010 Douglas A. Napoleone <doug.napoleone@gmail.com>.
# All rights reserved.
#
# i put it here because it dont want to install on Heroku.

# Licensed under the BSD License (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     https://code.google.com/p/python-simpleencode/source/browse/trunk/LICENSE
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

'''simple encode decode w/ private key, based on the base64 encode and decode.

Initially developed for turning database ID's into URL's without exposing the
ids in the url, or having a bot iterate over the values.

Also useful for storing passwords which need to be converted back to
clear text, in alphanumeric form given a secret word. This is NOT encryption
nor a hash. This is NOT cryptographically safe. For that an SSL public/private
key pair is preferred. For situations where the encoded string is already
protected by a privileged account, and the secret key is stored in a
configuration file which is also protected by a privileged login, this system
is secure. It is secure by virtue of having all its elements secure, and
mitigates the risk of compromise of either one of those vectors (but not both).

This is good for websites which store the secret key in a configuration file
on disk, and the encoded word in a database (accessible by a different user),
and where both values are not in transactional memory except for the duration
of decoding and using the decoded string, which should be immediate.
'''
VERSION = (1, 0, 0, "final")

def get_version():
    if VERSION[3] != "final":
        return "%s.%s.%s%s" % (VERSION[0], VERSION[1], VERSION[2], VERSION[3])
    else:
        return "%s.%s.%s" % (VERSION[0], VERSION[1], VERSION[2])

__version__ = get_version()
__author__ = 'Doug Napoleone <doug.napoleone@gmail.com>'
__all__ = ['mksecret', 'encode', 'decode']

from random import choice
from base64 import b64encode, b64decode
from string import printable, whitespace, letters, digits
from itertools import izip, cycle


safechars = ''.join(sorted(set(printable) - set(whitespace)))

def mksecret(length=50):
    '''return a secret key for encoding and hashing. (perfect for django!)'''
    return ''.join(choice(safechars) for i in xrange(length))

def xor(w1, w2):
    '''xor two strings together with the lenght of the first string limiting'''
    return ''.join(chr(ord(c1)^ord(c2)) for c1, c2 in izip(w1, cycle(w2)))

def encode(word, secret):
    '''safely encode a string given a secret key. This is not encryption as
    the same key is used for encoding and decoding, nor is it a hash as it is
    decodable. The word to be encoded is padded out with random data to
    the length of the secret key (longer keys are better). The returned string
    is even longer, and limited to alphaneumeric characters; perfect for
    storing in text files, urls, csv files, etc.

    for django DB id's use 'encode(str(id), django.config.settings.SECRET_KEY)'

    if being used for perminent URL's which do not change with successive
    calls to encode, a secret key of length 5 should be used, instead of
    the django secret key. This is safer as the encode call will always
    give the same result for a given input instead of padding out with data
    which could give away the pre-encoded data length.

    WARNING: This only works for strings shorter than 1000 characters.
    '''
    w = len(word)
    s = len(secret)
    base = "%.3d%s%s" % (w, secret[-1], word)
    b = len(base)
    if b < s:
        base += mksecret(s-b)
    return b64encode(xor(base, secret), '-_')

def decode(word, secret):
    '''decode the word which was encoded with the given secret key.
    '''
    base = xor(b64decode(word, '-_'), secret)
    return base[4:int(base[:3], 10)+4]
