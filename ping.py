from ripe.atlas.cousteau import Ping
from ripe.atlas.cousteau import AtlasSource

msm_id = 12345

from ripe.atlas.cousteau import AtlasStream

def on_result_response(*args):
    """
    Function that will be called every time we receive a new result.
    Args is a tuple, so you should use args[0] to access the real message.
    """
    print(args[0])

atlas_stream = AtlasStream()
atlas_stream.connect()

channel = "result"
# Bind function we want to run with every result message received
atlas_stream.bind_channel(channel, on_result_response)

# Subscribe to new stream for 1001 measurement results
stream_parameters = {"msm": msm_id, "type":"ping", }
atlas_stream.start_stream(stream_type="result", **stream_parameters)

# Make sure you have this line after you start *all* your streams
atlas_stream.timeout(seconds=86400)

# Shut down everything
atlas_stream.disconnect()
