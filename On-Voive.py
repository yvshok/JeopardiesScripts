import glob, struct, subprocess, os

# OneVoice
# Difficulty: Medium

# Following a few difficult quarters, Brunnerne A/S has implemented the app OneVoice across
# the organization to ensure a consistent approach to external communication
# Employees are, of course, free to speak for themselves...
# Corporate Communications simply asks that they always do so with OneVoice, using the weekly approved wording verbatim

# Lately, rumors have been spreading about an upcoming announcement that could affect a lot
# of employees and investors. Corporate has stayed silent, but maybe you can get ahead of the
# news if they already drafted the OneVoice message

comments = '''
  A mobile forensics utility designed to process custom encrypted binary resources
  extracted from Android raw application packages. Reconstructs and decrypts
  payload structures by emulating byte-level keystream XOR and rotation algorithms
'''

tags = '''
  #android #forensics #reverse_engineering #python #mobile
'''

class Py_testing:
  def rotate_right_8(self, val: int, count: int) -> int:
    val &= 0xFF
    count &= 0x7
    if count == 0: return val
    return ((val >> count) | (val << (8 - count))) & 0xFF

  def keystream_byte(self, index: int, table: bytes, salt: bytes) -> int:
    return table[index % len(table)] ^ salt[index % len(salt)]

  def decode(self, encoded: bytes, table: bytes, salt: bytes) -> bytes:
    ROTATION = 7
    decoded = bytearray(len(encoded))

    for i in range(len(encoded)):
      shift = (i % ROTATION) + 1
      rotated = self.rotate_right_8(encoded[i], shift)
      ks = self.keystream_byte(i, table, salt)
      decoded[i] = rotated ^ ks

    return bytes(decoded)

  def unpack(self, blob: bytes) -> list[bytes]:
    if not blob: return []

    COUNT = blob[0]
    OFFSET = 1
    chunks = []

    for _ in range(COUNT):
      if OFFSET + 2 > len(blob): break
      length = struct.unpack('>H', blob[OFFSET : OFFSET + 2])[0]
      OFFSET += 2

      if OFFSET + length > len(blob): break
      chunks.append(blob[OFFSET : OFFSET + length])
      OFFSET += length

    return chunks

  def main(self):
    # Algorithm constants extracted from decompiled Android components
    TABLE = bytes([63, 161, 8, 212, 98, 156, 23, 229, 75, 122, 195, 46, 145, 86, 189, 240])
    SALT = b"onevoice-2026-W27"

    subprocess.run('cp OnVoice.apk OnVioce.zip', shell=True)
    subprocess.run('unzip OnVioce.zip', shell=True)
    os.chdir('res')

    # Search stranges files into res/ directory, unzip the apk, the file is called kD.bin
    bin_files = glob.glob('*.bin')

    decoded_messages = []
    for bfile in bin_files:
      with open(bfile, 'rb') as f:
        raw_bytes = f.read()

      chunks = self.unpack(raw_bytes)
      for chunk in chunks:
        decrypted = self.decode(chunk, TABLE, SALT)
        try:
          decoded_messages.append(decrypted.decode('utf-8'))
        except Exception as e: pass

    decoded_text = ''.join(decoded_messages)
    print('Text:', decoded_text)

    # Flag => brunner{th3_dr4ft_sh1pp3d_w1th_th3_4ppr0v4l}

if __name__ == '__main__':
  Py_testing.main()
