from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import subprocess, base64, os

# Baked In
# Difficulty: Hard

# A local baker entered a baking contest, but something about the aftermath didn't add up...

comments = '''
  A forensics utility that extracts artifacts from a Linux memory dump via Volatility 3, carves embedded
  .NET DLLs from memory, decompiles them using ilspycmd, and decrypts an AES-CBC encrypted payload to reveal the flag
'''

tags = '''
  #memory-forensics #volatility3 #file-carving #dotnet #ilspycmd #aes-cbc #decryption
'''

class Py_testing:
  def main():
    # Dump the ecxel libreoffice file that contain the macro
    subprocess.run('python3 volatility3/vol.py --remote-isf-url "https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/banners/banners.json" -f mem.dump linux.pagecache.InodePages --inode 0x8b9ad7914108 --dump', shell=True)
    subprocess.run('mv inode_0x8b9ad7914108.dmp results-from-judges.ods', shell=True)

    # Dump the /tmp/.gnome-scache file mentioned inside the macro
    subprocess.run('python3 volatility3/vol.py --remote-isf-url "https://github.com/Abyss-W4tcher/volatility3-symbols/raw/master/banners/banners.json" -f mem.dump linux.pagecache.InodePages --inode 0x8b9b42a40670 --dump', shell=True)
    subprocess.run('mv inode_0x8b9b42a40670.dmp gnome-scache', shell=True)
    os.makedirs('hidden_dlls')
    os.chdir('hidden_dlls')

  def found_dlls():
    with open('gnome-scache', 'rb') as f:
      data = f.read()

    FOUND_DLL = 0
    IDX = 0

    while True:
      # Search the Bundle Header signature of .NET (Bundle Manifest)
      IDX = data.find(b'BSJB', IDX)
      if IDX == -1: break

      # Search MZ / PE headers (0x4D 0x5A)
      pe_start = data.rfind(b'MZ', 0, IDX)
      if pe_start != -1:
        # Extract the aprox size of DLL or read until the next MZ / PE headers (0x4D 0x5A)
        dll_data = data[pe_start:pe_start + 500000] # 500KB aprox
        out_path = f'hidden_{FOUND_DLL}.dll'

        with open(out_path, 'wb') as out:
          out.write(dll_data)

        found_dlls += 1
      IDX += 4

  def decode_payload():
    subprocess.run('dotnet tool install -g ilspycmd', shell=True)
    subprocess.run('ilspycmd -p -o . extracted_6.dll', shell=True)

    with open('Program.cs', 'r') as gnome_helper:
      content = gnome_helper.readlines()

    KEY = content[8].split('"')[1].encode()
    IV = content[10].split('"')[1].encode()
    CTB64 = 'iAOC5E/kZo090/MaLKq0F4TXhdQ77V1QBOxGVg/2t5eAuFlSKXjpFmjgIlOwLM0y'

    ciphertext = base64.b64decode(CTB64)

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV))
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    print("FLAG:", decrypted.decode('utf-8').strip())

  # flag => brunner{h1dd3n_1ngr3d13nts_1n_th3_r3c1p3}

if __name__ == '__main__':
  Py_testing.main()
  Py_testing.found_dlls()
  Py_testing.decode_payload()
