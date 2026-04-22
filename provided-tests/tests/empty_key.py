import requests

from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def empty_key(conductor: ClusterConductor, dir, log: Logger):
    """
    The spec says key matches [0-9a-zA-Z-]{0,128} which allows
    a zero-length key. PUT /data/ and GET /data/ should work.
    """
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        base_url = fx.clients[0].base_url

        # PUT with empty key
        r = requests.put(
            f"{base_url}/data/",
            data="empty-key-value",
            headers={"Content-Type": "text/plain"},
            timeout=10,
        )
        assert r.status_code == 200, (
            f"expected PUT /data/ status 200, got {r.status_code}"
        )

        # GET with empty key
        r = requests.get(f"{base_url}/data/", timeout=10)
        assert r.status_code == 200, (
            f"expected GET /data/ status 200, got {r.status_code}"
        )
        assert r.text == "empty-key-value", (
            f"expected body 'empty-key-value', got '{r.text}'"
        )

        conductor.dump_all_container_logs(dir)

    return True, "ok"
