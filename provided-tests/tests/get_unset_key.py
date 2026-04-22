from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def get_unset_key(conductor: ClusterConductor, dir, log: Logger):
    """
    GET a key that was never PUT.
    Spec: status MUST be 404 AND body MUST be empty.
    """
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]

        r = client.get("never-set-key")
        assert r.status_code == 404, (
            f"expected 404, got {r.status_code}"
        )
        assert r.text == "", (
            f"expected empty body, got {r.text!r}"
        )

        conductor.dump_all_container_logs(dir)

    return True, "ok"
