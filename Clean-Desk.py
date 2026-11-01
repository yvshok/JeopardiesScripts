import base64
from Crypto.Cipher import AES

# CleanDesk
# Difficulty: Easy-Medium

# A colleague left Brunnerne A/S on a Friday, and the handover was shorter than anyone would have liked
# IT imaged her phone before wiping it, which is policy, and filed the image on the shared drive,
# which is not. Every app on that device encrypts its data at rest. IT confirmed this in the offboarding ticket and closed it

comments = '''
  A small utility that decrypts AES-GCM records stored as Base64 strings,
  extracts the nonce, authentication tag & ciphertext, & reconstructs the decrypted content
'''

tags = '''
  #aes #gcm #base64 #crypto #python #decrypt
'''

class Py_testing:
  def main():
    KEY = base64.b64decode("6mqMbv76RDT1G7yib5XrsS5DolJ+pPfZAGacZN3cTsc=")

    def decrypt_gcm_record(b64_data):
      raw = base64.b64decode(b64_data.strip())

      # <string name="content_key">6mqMbv76RDT1G7yib5XrsS5DolJ+pPfZAGacZN3cTsc=</string>
      # <string name="content_key_alg">AES-256-GCM</string>
      # <string name="sealed_layout">nonce[12] || ciphertext || tag[16]</string>
      # <string name="sealed_aad">none</string>

      NONCE = raw[:12]
      TAG = raw[-16:]
      CT = raw[12:-16]

      ciphertext = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)

      try:
        return ciphertext.decrypt_and_verify(CT, TAG)
      except Exception as e:
        # Retry with literal b"none" as AAD
        ciphertext = AES.new(KEY, AES.MODE_GCM, nonce=NONCE)
        ciphertext.update(b"none")
        return ciphertext.decrypt_and_verify(CT, TAG)

    # The ciphertext data is inside notes.db
    with open("notes_db_content.txt", "r") as seal_file:
      data = seal_file.readlines()

    decrypted_output = bytearray()

    for i, line in enumerate(data):
      line = line.strip()

      if not line: continue

      try: decrypted_output.extend(decrypt_gcm_record(line))
      except Exception as e: pass

    print(decrypted_output.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
  Py_testing.main()
