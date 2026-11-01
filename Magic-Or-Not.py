import glob

# Magic or not
# Difficulty: Easy

# As an intern at Brunner Corporation, I developed a cutting-edge image obfuscation algorithm, designed
# to hide sensitive image data. I'm confident it's secure, but
# the security team isn't convinced, they believe custom cryptography always hides a flaw

# Can you prove them wrong? Analyze the implementation, recover the original image, and find the flag

comments = '''
  A digital forensics utility designed to process custom obfuscated image files extracted
  from CTF challenge resources. Reconstructs and decrypts image formats
  by deriving byte-level single-byte XOR key signatures from known magic headers
'''

tags = '''
  #stego #forensics #reverse_engineering #python #cryptography
'''

class Py_testing:
  def derive_key(self, raw_bytes: bytes, filename: str) -> int:
    if filename.endswith('.png'): expected = b'\x89'
    elif filename.endswith('.jpg') or filename.endswith('.jpeg'): expected = b'\xFF'
    elif filename.endswith('.gif'): expected = b'G'
    elif filename.endswith('.bmp'): expected = b'B'
    else: expected = b'\x89'

    return raw_bytes[0] ^ expected[0]

  def decode(self, encoded: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in encoded])

  def main(self):
    # Known magic headers for standard image files
    IMG_EXT = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
    image_files = []

    for ext in IMG_EXT: image_files.extend(glob.glob(ext))

    image_files = [f for f in image_files if not f.startswith('recovered_')]

    for img_file in image_files:
      with open(img_file, 'rb') as f:
        raw_bytes = f.read()

      if not raw_bytes: continue

      KEY = self.derive_key(raw_bytes, img_file)
      decrypted = self.decode(raw_bytes, KEY)

      out_filename = f"recovered_{img_file}"
      with open(out_filename, 'wb') as f:
        f.write(decrypted)

    # Flag => brunner{ctf2026}

if __name__ == '__main__':
  Py_testing.main()
