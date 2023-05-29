
import requests
import sounddevice as sd
import numpy as np
from resemble import Resemble
  
Resemble.api_key('HvBlf5QgzvA8PxyoOs3w8gtt')
# Resemble AI API endpoint
Resemble.syn_server_endpoint= "http://f.cluster.resemble.ai/stream"

# Resemble AI API key
api_key = 'HvBlf5QgzvA8PxyoOs3w8gtt'

# Text to be synthesized
text = "Hello, this is a test message."

# Request payload
Response = Resemble.v2.clips.stream(project_uuid="7cd5e72b",voice_uuid="b2d1bb75",body="Streaming helps deliver synthesized audio before it's entirely ready.")
for res in Response:
    print(res)
