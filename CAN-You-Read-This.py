import subprocess

# CAN you read this
# Difficulty: Hard

# We extracted a CAN bus recording from the Brunnerne Inc.™ company car
# The driver is suspected of sharing company secrets through the car, somehow. Find the secret message

# Note: Submit the secret message in lowercase with spaces replaced by _, wrapped in brunner{}
# Example: If you find the message "This is the secret", you should submit brunner{this_is_the_secret}

comments = '''
  A small utility that processes CAN bus log records to extract payload bytes,
  counts pulse sequences to reconstruct Morse code signals, and decodes the message
'''

tags = '''
  #canbus #morse #forensics #ctf #python #subprocess
'''

MORSE_CODE_DICT = {
  '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'
}

class Py_testing:
  def main():
    subprocess.run('asc2log -I can-recording-model-3.asc -O can_bus.log', shell=True)
    # Execute terminal command to capture target CAN bus ID entries
    STD_OUT = subprocess.run("cat can_bus.log | grep '3F5#'", shell=True, capture_output=True, text=True)

    # Extract only the hexadecimal payload from each CAN frame
    lines = STD_OUT.stdout.strip().split('\n')
    content = []
    for line in lines:
      if '#' in line:
        payload = line.split('#')[1].split()[0]
        content.append(payload)

    # Frame identifiers representing silence vs active pulse
    IGNOTE_STR = '0000C838820C0000'
    JUMP_STR = '0000C81892040000'

    tokens = []
    current_type = None
    current_count = 0

    # Group continuous consecutive sequences into tokens
    for line in content:
      if line == JUMP_STR:
        if current_type == 'jump': current_count += 1
        else:
          if current_type is not None: tokens.append((current_type, current_count))
          current_type = 'jump'
          current_count = 1
      elif line == IGNOTE_STR:
        if current_type == 'ignore': current_count += 1
        else:
          if current_type is not None: tokens.append((current_type, current_count))
          current_type = 'ignore'
          current_count = 1

    if current_type is not None:
      tokens.append((current_type, current_count))

    # Convert continuous tokens into Morse symbols using threshold rules:
    # <=3 jumps = dot (.), >3 jumps = dash (-), >=9 ignores = space ( )
    morse_stream = []
    for token_type, count in tokens:
      if token_type == 'jump':
        if count <= 3: morse_stream.append('.')
        else: morse_stream.append('-')
      elif token_type == 'ignore':
        if count >= 9: morse_stream.append(' ')

    # Translate extracted Morse symbols into human-readable text
    raw_morse = ''.join(morse_stream).strip()
    letters_morse = raw_morse.split(' ')

    decoded_text = []
    for char in letters_morse:
      if char in MORSE_CODE_DICT: decoded_text.append(MORSE_CODE_DICT[char])
      elif char == '': decoded_text.append(' ')
      else: decoded_text.append('?')

    print('Morse:', raw_morse)
    print('Texto:', ''.join(decoded_text))

if __name__ == '__main__':
  Py_testing.main()
