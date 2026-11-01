import base64
import zstandard as zstd
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# The Missing Recipe
# Difficulty: Medium

# Brunner Corporation's research department has discovered that some inappropriate Brunner
# images and a confidential internal recipe have disappeared from the network

# No one knows exactly when or how it happened, but several employees reported unusual
# network activity around the time of the incident

# Fortunately, Brunner Corporation's Security Operations Center (SOC) has a full network
# capture (PCAP) from the period. However, the analysts have been unable to determine what really happened

# Can you reconstruct the attack and recover the flag?
# Please do not look at the pictures

comments = '''
  A small utility that decodes Base32-encoded compressed chunks,
  decompresses the data with Zstandard and decrypts the second chunk using AES-CBC
'''

tags = '''
  #base32 #zstandard #aes #cbc #crypto #python
'''

class Py_testing:
  def main():
    # The key apect to devide both chunks is this fc2s77
    CHUNK_1 = ['fc2s77jar2gqgafci4mbu4clou2gfciqcerci', 'lmng3ntqmsxaq6prsqh6sxsoasodd6ng7', 'duzfupucvdeillyi5ljlkb6afiqwyfrjnay5pnklod', 'qoxtixy7ehdpwja3jtornpdzu2jj6ytgrasxv4', '5hxgw3orxpsqbhpoe5erkscaqeabosaecyavwisqqj4yjq']
    CHUNK_2 = ['fc2s77laaaaaccaaawssaz5yzsflg72nnx22cvaj6s55', '5mlpk3pxrnxylqcen2zxo6qb444dug4lpqbgvqmi2vusir5hkq', 'jeqx2io53yrgk6y7wn6bht6s7aogmxh66a6xjytmn', '3j4iya4bqkzebuwup56b26juiwwkefh3yf5', 'pnucvyn4jxwhwxpotatrtyjkt7cu4vlzga5evd72b', 'p2epbp6ywvt4tfvvndripkc57eo5vsdor2ejefs4a', 'sfjoijdi7nk6xb4eb7dwaqd6ojaro56qyj4g', 'vszaghqmrticvg2wkgsoh556dd7vsb3yg3pgay', '54ianusrqrf2pxckbrjoiyqgq6oqjphrfxt55c2albqkln4wna', 'rspvrbpw7t3t4zo4wc3sh7svfun4mgxl6v4675jru4nl5cahnq']

    def base_decode(name, chunks):
      # Join the Base32 fragments into a single encoded blob
      BLOB = ''.join(chunks).upper()

      # Add Base32 padding when the encoded length is not aligned
      pad = (-len(BLOB)) % 8
      padded = BLOB + '=' * pad

      decoded_text = base64.b32decode(padded)

      # Initialize the Zstandard decompression context
      decompress_text = zstd.ZstdDecompressor()
      out = decompress_text.decompress(decoded_text)

      return out

    content_1 = base_decode('chunk_1', CHUNK_1)
    content_2 = base_decode('chunk_2', CHUNK_2)

    print('CHUNK_1:', content_1.decode())

    # The key is send by one chunk as base32 in TXT DNS record
    KEY = b'Brunn3rK3yAESCBC'
    IV = content_2[:16]
    CT = content_2[16:]

    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    decrypted_text = unpad(cipher.decrypt(CT), 16)

    print('CHUNK_2:', decrypted_text.decode())

  # Flag => brunner{k33p_53nd1ng_th3_me55ag3s}

if __name__ == '__main__':
  Py_testing.main()
