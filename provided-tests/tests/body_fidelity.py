from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def body_fidelity(conductor: ClusterConductor, dir, log: Logger):
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]

        cases = [
            ("fidelity-spaces", "  spaces around  "),
            ("fidelity-newlines", "line1\nline2\nline3"),
            ("fidelity-plain", "just plain text, not json"),
            ("fidelity-empty", ""),
        ]

        for key, value in cases:
            r = client.put(key, value)
            assert r.status_code == 200, (
                f"PUT {key}: expected 200, got {r.status_code}"
            )

            r = client.get(key)
            assert r.status_code == 200, (
                f"GET {key}: expected 200, got {r.status_code}"
            )
            assert r.text == value, (
                f"GET {key}: expected {value!r}, got {r.text!r}"
            )
            log(f"  {key}: ok")

        conductor.dump_all_container_logs(dir)

    return True, "ok"
