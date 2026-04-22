import requests

from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def view_double_put(conductor: ClusterConductor, dir, log: Logger):
    """
    Send two different PUT /view requests. The second should
    overwrite the first. Both must return 200 with empty body.
    """
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]
        base_url = client.base_url

        view_1 = {
            "defaultShard": [{"address": "10.0.0.1:8081", "id": 1}]
        }
        view_2 = {
            "defaultShard": [
                {"address": "10.0.0.2:8081", "id": 2},
                {"address": "10.0.0.3:8081", "id": 3},
            ]
        }

        # first PUT /view
        r = requests.put(f"{base_url}/view", json=view_1, timeout=10)
        assert r.status_code == 200, (
            f"first PUT /view: expected 200, got {r.status_code}"
        )
        assert r.text == "" or r.text is None, (
            f"first PUT /view: expected empty body, got {r.text!r}"
        )

        # second PUT /view (overwrite)
        r = requests.put(f"{base_url}/view", json=view_2, timeout=10)
        assert r.status_code == 200, (
            f"second PUT /view: expected 200, got {r.status_code}"
        )
        assert r.text == "" or r.text is None, (
            f"second PUT /view: expected empty body, got {r.text!r}"
        )

        conductor.dump_all_container_logs(dir)

    return True, "ok"
