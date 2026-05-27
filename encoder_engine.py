import base64, codecs, html, binascii
from urllib.parse import quote, unquote

MORSE_ENC = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    ' ':'/'
}
MORSE_DEC = {v: k for k, v in MORSE_ENC.items()}

def _morse_enc(text):
    result = []
    for ch in text.upper():
        result.append(MORSE_ENC[ch] if ch in MORSE_ENC else '?')
    return ' '.join(result)

def _morse_dec(text):
    result = []
    for token in text.strip().split(' '):
        if token == '/':
            result.append(' ')
        elif token in MORSE_DEC:
            result.append(MORSE_DEC[token])
    return ''.join(result)

ALGORITHMS = {
    'UTF-8 Hex': {
        'desc': 'Encodes text to UTF-8 and represents bytes as hexadecimal',
        'enc': lambda t: t.encode('utf-8').hex(),
        'dec': lambda t: bytes.fromhex(t.replace(' ','')).decode('utf-8'),
    },
    'UTF-16 Hex': {
        'desc': 'Encodes text to UTF-16 (with BOM) and represents bytes as hex',
        'enc': lambda t: t.encode('utf-16').hex(),
        'dec': lambda t: bytes.fromhex(t.replace(' ','')).decode('utf-16'),
    },
    'UTF-32 Hex': {
        'desc': 'Encodes text to UTF-32 (with BOM) and represents bytes as hex',
        'enc': lambda t: t.encode('utf-32').hex(),
        'dec': lambda t: bytes.fromhex(t.replace(' ','')).decode('utf-32'),
    },
    'ASCII Hex': {
        'desc': 'Encodes ASCII text into hexadecimal character codes',
        'enc': lambda t: t.encode('ascii').hex(),
        'dec': lambda t: bytes.fromhex(t.replace(' ','')).decode('ascii'),
    },
    'CP1251 Hex': {
        'desc': 'Encodes text to Windows-1251 (Cyrillic) and represents as hex',
        'enc': lambda t: t.encode('cp1251').hex(),
        'dec': lambda t: bytes.fromhex(t.replace(' ','')).decode('cp1251'),
    },
    'Base64': {
        'desc': 'Standard Base64 encoding (RFC 4648)',
        'enc': lambda t: base64.b64encode(t.encode('utf-8')).decode(),
        'dec': lambda t: base64.b64decode(t.encode()).decode('utf-8'),
    },
    'Base64 URL': {
        'desc': 'URL-safe Base64 variant used in JWT and URLs',
        'enc': lambda t: base64.urlsafe_b64encode(t.encode('utf-8')).decode(),
        'dec': lambda t: base64.urlsafe_b64decode(t.encode()).decode('utf-8'),
    },
    'Base32': {
        'desc': 'Base32 encoding (RFC 4648) — uses characters A-Z and 2-7',
        'enc': lambda t: base64.b32encode(t.encode('utf-8')).decode(),
        'dec': lambda t: base64.b32decode(t.encode()).decode('utf-8'),
    },
    'Base16 (HEX)': {
        'desc': 'Base16 encoding — same as HEX but via RFC 4648 standard',
        'enc': lambda t: base64.b16encode(t.encode('utf-8')).decode(),
        'dec': lambda t: base64.b16decode(t.encode()).decode('utf-8'),
    },
    'Binary': {
        'desc': 'Represents each UTF-8 byte in binary form (8 bits)',
        'enc': lambda t: ' '.join(format(b, '08b') for b in t.encode('utf-8')),
        'dec': lambda t: bytes(int(x, 2) for x in t.split()).decode('utf-8'),
    },
    'Octal': {
        'desc': 'Represents each UTF-8 byte in octal form',
        'enc': lambda t: ' '.join(format(b, '03o') for b in t.encode('utf-8')),
        'dec': lambda t: bytes(int(x, 8) for x in t.split()).decode('utf-8'),
    },
    'Unicode Escape': {
        'desc': 'Represents characters as \\uXXXX (Python unicode escape)',
        'enc': lambda t: t.encode('unicode_escape').decode('ascii'),
        'dec': lambda t: t.encode('ascii').decode('unicode_escape'),
    },
    'URL Encoding': {
        'desc': 'Percent-encoding (RFC 3986) — used in URLs and HTTP',
        'enc': lambda t: quote(t, safe=''),
        'dec': lambda t: unquote(t),
    },
    'HTML Entities': {
        'desc': 'Encodes special characters as HTML entities (&amp; &lt; etc.)',
        'enc': lambda t: html.escape(t),
        'dec': lambda t: html.unescape(t),
    },
    'ROT13': {
        'desc': 'Shifts Latin letters by 13 positions (symmetric)',
        'enc': lambda t: codecs.encode(t, 'rot_13'),
        'dec': lambda t: codecs.encode(t, 'rot_13'),
    },
    'Morse': {
        'desc': 'Morse code — encodes Latin letters and digits with dots and dashes',
        'enc': _morse_enc,
        'dec': _morse_dec,
    },
    'Caesar (shift 13)': {
        'desc': 'Caesar cipher with fixed shift of 13 for Latin letters',
        'enc': lambda t: ''.join(
            chr((ord(c)-65+13)%26+65) if c.isupper() and c.isascii() else
            chr((ord(c)-97+13)%26+97) if c.islower() and c.isascii() else c
            for c in t),
        'dec': lambda t: ''.join(
            chr((ord(c)-65-13)%26+65) if c.isupper() and c.isascii() else
            chr((ord(c)-97-13)%26+97) if c.islower() and c.isascii() else c
            for c in t),
    },
    'Atbash': {
        'desc': 'Atbash cipher — mirror substitution of letters (A↔Z, B↔Y…)',
        'enc': lambda t: ''.join(
            chr(90-(ord(c)-65)) if c.isupper() and c.isascii() else
            chr(122-(ord(c)-97)) if c.islower() and c.isascii() else c
            for c in t),
        'dec': lambda t: ''.join(
            chr(90-(ord(c)-65)) if c.isupper() and c.isascii() else
            chr(122-(ord(c)-97)) if c.islower() and c.isascii() else c
            for c in t),
    },
}

CATEGORIES = {
    'Character Encodings': ['UTF-8 Hex', 'UTF-16 Hex', 'UTF-32 Hex', 'ASCII Hex', 'CP1251 Hex'],
    'Base Encodings': ['Base64', 'Base64 URL', 'Base32', 'Base16 (HEX)'],
    'Numeric Representations': ['Binary', 'Octal', 'Unicode Escape'],
    'Web Encodings': ['URL Encoding', 'HTML Entities'],
    'Classical Ciphers': ['ROT13', 'Morse', 'Caesar (shift 13)', 'Atbash'],
}

def encode(algo: str, text: str) -> str:
    return ALGORITHMS[algo]['enc'](text)

def decode(algo: str, text: str) -> str:
    return ALGORITHMS[algo]['dec'](text)
