import asyncio

from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def concurrent_puts_distinct_keys(conductor: ClusterConductor, dir, log: Logger):
    """
    Fire 100 concurrent PUTs, each to a different key, via asyncio.gather.
    All PUTs must return 200, and every subsequent GET must return
    the exact value that was written for that key.

    This catches the failure mode where a server stores state in
    per-thread/per-worker dictionaries: a GET landing on a different
    worker than the PUT would miss the key.
    """
    N = 100

    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]
        pairs = [(f"key-{i}", f"value-{i}") for i in range(N)]

        async def run():
            put_results = await asyncio.gather(
                *(asyncio.to_thread(client.put, k, v) for k, v in pairs)
            )
            for (k, _), r in zip(pairs, put_results):
                assert r.status_code == 200, (
                    f"concurrent PUT for {k!r}: expected 200, got {r.status_code}"
                )

            get_results = await asyncio.gather(
                *(asyncio.to_thread(client.get, k) for k, _ in pairs)
            )
            for (k, v), r in zip(pairs, get_results):
                assert r.status_code == 200, (
                    f"GET for {k!r}: expected 200, got {r.status_code}"
                )
                assert r.text == v, (
                    f"GET for {k!r}: expected {v!r}, got {r.text!r}"
                )

        asyncio.run(run())

        conductor.dump_all_container_logs(dir)

    return True, "ok"
