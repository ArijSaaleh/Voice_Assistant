from deepgram import Deepgram
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
# Your Deepgram API Key
DEEPGRAM_API_KEY = os.getenv('API_KEY')

# URL for the audio you would like to stream
# URL for the example resource will change depending on whether user is outside or inside the UK
# Outside the UK
URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourlw_online_nonuk'
# Inside the UK
# URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm'

async def main():
  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  # Create a websocket connection to Deepgram
  # In this example, punctuation is turned on, interim results are turned off, and language is set to US English.
  try:
    deepgramLive = await deepgram.transcription.live({ 'punctuate': True, 'interim_results': False, 'language': 'en-US' })
  except Exception as e:
    print(f'Could not open socket: {e}')
    return

# Listen for the connection to close
  deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

  # Listen for any transcripts received from Deepgram and write them to the console
  deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, print)
  
  # Listen for the connection to open and send streaming audio from the URL to Deepgram
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as audio:
      while True:
        data = await audio.content.readany()
        deepgramLive.send(data)

        # If there's no data coming from the livestream then break out of the loop
        if not data:
            break

  # Indicate that we've finished sending data by sending the customary zero-byte message to the Deepgram streaming endpoint, and wait until we get back the final summary metadata object
  await deepgramLive.finish()

asyncio.run(main())