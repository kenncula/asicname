from ripe.atlas.cousteau import Ping
from ripe.atlas.cousteau import AtlasSource

ping = Ping(
    af="4",
    target="google.com",
    description="Ping Test"
)

sources = AtlasSource(
    type="probes",
    value="[]",
    requested=32,
)

