import asyncio

from ..utils.containers import ClusterConductor
from ..utils.kvs_api import KVSTestFixture
from ..utils.util import Logger


def concurrent_puts(conductor: ClusterConductor, dir, log: Logger):
    """
    Fire two PUTs to the same key concurrently via asyncio.gather.
    Both should return 200. A subsequent GET must return
    exactly one of the two values (not garbage, not empty).
    Repeated GETs must be stable.
    """
    with KVSTestFixture(conductor, dir, log, node_count=1) as fx:
        client = fx.clients[0]
        key = "concurrent-test"
        val_a = "value_a"
        val_b = "value_b"

        async def run():
            put_results = await asyncio.gather(
                asyncio.to_thread(client.put, key, val_a),
                asyncio.to_thread(client.put, key, val_b),
            )
            for r in put_results:
                assert r.status_code == 200, (
                    f"concurrent PUT: expected 200, got {r.status_code}"
                )

            # GET should return one of the two values
            r = await asyncio.to_thread(client.get, key)
            assert r.status_code == 200, (
                f"GET after concurrent PUTs: expected 200, got {r.status_code}"
            )
            assert r.text in (val_a, val_b), (
                f"GET returned {r.text!r}, expected one of {val_a!r} or {val_b!r}"
            )
            winner = r.text
            log(f"  winner: {winner!r}")

            # repeated GETs should be stable
            repeat_results = await asyncio.gather(
                *(asyncio.to_thread(client.get, key) for _ in range(3))
            )
            for i, r in enumerate(repeat_results):
                assert r.status_code == 200
                assert r.text == winner, (
                    f"GET #{i} returned {r.text!r}, expected stable {winner!r}"
                )

        asyncio.run(run())

        conductor.dump_all_container_logs(dir)

    return True, "ok"
