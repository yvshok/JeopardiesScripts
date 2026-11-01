# Free Play
# Difficulty: Easy-Medium

# IT flagged a workstation during an asset audit and found that someone from Procurement
# had installed some game from 2009 on his corporate laptop. Apparently, he was obsessed with
# the game and had been "working from home" for three weeks, seemingly just staring at his character roster
# HR wants to know what he was doing and luckily recovered his save file along with a screenshot from the backup share
# Go figure out what is so special about this save file

# Flag format: The flag is found as a string with underscores, wrap the text in brunner{<text>}
# Example: if you found the flag text_here, the flag to submit would be brunner{text_here}

# Note: This challenge is fully solvable from the handout. Please do not attempt to obtain a game copy illegally!

comments = '''
  A small utility that reads raw binary offsets from a SaveGame file,
  mapping null/byte values (0x00 and 0x03) into binary bitstreams (0 and 1) to
  recover hidden memory structures
'''

tags = '''
  #xxd #binary #savegame #reverse-engineering #ctf
'''

class Py_testing:
  def main():
    # Offsets recovered using xxd command
    OFFSET_START=0x9D20
    OFFSET_END=0x9DC0

    resultado_bits = []

    with open('SaveGame1', 'rb') as f:
      f.seek(OFFSET_START)
      bytes_data = f.read(OFFSET_END - OFFSET_START)

      for b in bytes_data:
        if b == 0x00: resultado_bits.append('0')
        elif b == 0x03: resultado_bits.append('1')

    print(''.join(resultado_bits))

    # Flag => brunner{strong_force_in_you}

if __name__ == '__main__':
  Py_testing.main()
