import gzip, subprocess, os, sys, base64
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES
from Crypto.Cipher import AES

# Interstellar C2
# Difficulty: Medium

# We noticed some interesting traffic coming from outer space. An unknown group is using
# a Command and Control server. After an exhaustive investigation, we discovered
# they had infected multiple scientists from Pandora's private research lab. Valuable
# research is at risk. Can you find out how the server works and retrieve what was stolen?

comments = '''
  A network forensics utility that parses a PCAP capture (capture.pcapng) using tshark to extract HTTP payloads
  exfiltrated by a PoshC2 framework. It reconstructs the dynamic key-exchange mechanism, decrypts AES-CBC
  encrypted stages and loaded modules (such as SharpSploit), and decompresses (gzip/base64)
  the final exfiltrated exfiltration artifact containing the flag
'''

tags = '''
  #pcap #tshark #poshc2 #aes-cbc #decryption #c2 #base64 #gzip
'''

class Py_testing:
  def get_94974f08_5853_41ab_938a_ae1bd86d8e51():
    # The vn48.ps1 is downloading a PE file from /94974f08-5853-41ab-938a-ae1bd86d8e51
    subprocess.run('tshark -r capture.pcapng -T fields -Y "frame.number == 62" -e http.file_data | xxd -p -r > tmp7102591.bin', shell=True)

    KEY = bytearray([0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0])
    IV = bytearray([0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1])

    with open('tmp7102591.bin', 'rb') as ct_file:
      ciphertext = ct_file.read()

    cipher = AES.new(bytes(KEY), AES.MODE_CBC, bytes(IV))
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open("tmp7102591.exe", "wb") as dc_file:
      dc_file.write(decrypted_data)

  def main():
    def decrypt_aes(base64_ct, key):
      raw = base64.b64decode(base64_ct.strip())
      iv, ciphertext = raw[:16], raw[16:]

      cipher = AES.new(base64.b64decode(key), AES.MODE_CBC, iv)
      decrypted = cipher.decrypt(ciphertext).rstrip(b'\x00')

      # If there, try to decode another base64 layer
      try:
        return base64.b64decode(decrypted.strip())
      except Exception as e: pass

    def decode_enc1():
      KEY = 'DGCzi057IDmHvgTVE2gm60w8quqfpMD+o8qCBGpYItc='

      # The ciphertext is get through /Kettie/Emmie/Anni?Theda=Merrilee?c
      subprocess.run('tshark -r capture.pcapng -T fields -Y "frame.number == 80" -e http.file_data | xxd -p -r > enc1.bin', shell=True)

      with open('enc1.bin', 'rb') as enc_file:
        content = enc_file.read()

      decrypted_enc = decrypt_aes(content, KEY).decode().split()

      for x in decrypted_enc:
        if x.startswith('NEWKEY8839394'):
          return x.replace('NEWKEY8839394','').replace('4939388YEKWEN', '')

    KEY = decode_enc1()

    def decode_enc2():
      # The ciphertext is get through /Kikelia/Jacinthe/Adorne/Kariotta/Lonee/Krystalle/4b6ab472-7d73-4a7e-95d0-2f691d8424dc/?dVfhJmc2ciKvPOC
      subprocess.run('tshark -r capture.pcapng -T fields -Y "frame.number == 468" -e http.file_data | xxd -p -r > enc2.bin', shell=True)

      with open('enc2.bin', 'rb') as enc_file:
        content = enc_file.read()

      decrypted_enc = decrypt_aes(content, KEY).decode().replace('multicmd00031loadmodule', '').replace('multicmd00034loadmodule', '').replace('!d-3dion@LD!-d00033loadpowerstatus', '').replace('!d-3dion@LD!-d00035run-dll SharpSploit.Credentials.Mimikatz SharpSploit Command "privilege::debug sekurlsa::logonPasswords"', '').strip()
      decrypted_enc = base64.b64decode(decrypted_enc)

      with open("poshC2.exe", "wb") as dec_file:
        dec_file.write(decrypted_enc)

    def decode_enc3():
      # The ciphertext is get through /Fanchette/Marlyn/Casey/Bobbye/Elayne/Charmane/2e392cdf-4b4e-44e8-891d-d00acbbf9736/?dVfhJmc2ciKvPOC
      subprocess.run('tshark -r capture.pcapng -T fields -Y "frame.number == 5953" -e http.file_data | xxd -p -r > enc3.bin', shell=True)

      with open('enc3.bin', 'rb') as enc_file:
        content = enc_file.read()

      decrypted_enc = decrypt_aes(content, KEY).decode().replace('multicmd00031loadmodule', '').replace('multicmd00034loadmodule', '').replace('!d-3dion@LD!-d00033loadpowerstatus', '').replace('!d-3dion@LD!-d00035run-dll SharpSploit.Credentials.Mimikatz SharpSploit Command "privilege::debug sekurlsa::logonPasswords"', '').strip()
      decrypted_enc = base64.b64decode(decrypted_enc)

      with open('sharesploit.exe', 'wb') as dec_file:
        dec_file.write(decrypted_enc)

    def decode_main_post():
      # The ciphertext is get through /Glennis/Elfrieda/Fannie/Nola/Janetta/Darda/Kathi/Britte?Berta=Lidia771d627d-d2ae-4337-aa81-96ec483eba07/?dVfhJmc2ciKvPOC
      subprocess.run('tshark -r capture.pcapng -T fields -Y "frame.number == 7242" -e http.file_data | xxd -p -r > glennis.bin', shell=True)

      with open('glennis.bin', 'rb') as enc_file:
        content = enc_file.read()[1500:]

      IV = content[:16]
      DATA = content[16:]

      cipher = AES.new(base64.b64decode(KEY), AES.MODE_CBC, iv=IV)
      clean = cipher.decrypt(DATA)
      uc = gzip.decompress(clean)

      with open('glennis.png', 'wb') as dec_file:
        dec_file.write(base64.b64decode(uc))

    decode_enc2()
    decode_enc3()
    decode_main_post()

    # Flag => HTB{h0w_c4N_y0U_s3e_p05H_c0mM4nd?}

if __name__ == '__main__':
  Py_testing.main()
