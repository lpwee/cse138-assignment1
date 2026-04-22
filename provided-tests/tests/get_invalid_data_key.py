from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSClient, KVSTestFixture
from ..utils.util import Logger


def get_invalid_data_key(conductor: ClusterConductor, dir, log: Logger):
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]

        r = client.get("test1") # GET key without setting before
        assert r.status_code == 404, (
            f"expected get status code to be 404, got {r.status_code}"
        )

        conductor.dump_all_container_logs(dir)

        # return score/reason
        return True, "ok"
