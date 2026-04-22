from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def two_puts_get_latest(conductor: ClusterConductor, dir, log: Logger):
    """
    PUT a key twice, then GET. Spec says GET must return
    'the most recently acknowledged PUT request's body'.
    """
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]

        r = client.put("overwrite-key", "first")
        assert r.status_code == 200, (
            f"first PUT: expected 200, got {r.status_code}"
        )

        r = client.put("overwrite-key", "second")
        assert r.status_code == 200, (
            f"second PUT: expected 200, got {r.status_code}"
        )

        r = client.get("overwrite-key")
        assert r.status_code == 200, (
            f"GET: expected 200, got {r.status_code}"
        )
        assert r.text == "second", (
            f"GET: expected 'second', got {r.text!r}"
        )

        conductor.dump_all_container_logs(dir)

    return True, "ok"
