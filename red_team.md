/ping

with non-empty body, how should it respond? i'd say 200 ok; no code change needed

with header, how should it respond? i'd say assert 200 ok; no code change needed

/view

two view PUT requests, how should it respond? overrwrite previous? add to dict?

invalid header format, how should it respond? assert

invalid body format, how should it respond? assert

/data

no key 

- [v] GET key that hasnt been initialised, should 404

invalid header

invalid body

long key

illegal character key

two PUT, asert GET gets latest











maybe need mutex for KVStore? what if sent 100 requests all reading and writing at the same time? 

spamming write(put) requests with the same key amd different values, to test race condition

- 404 test
- concurrent requests, 100 puts each to a different key using async/gather
    - if server has 4 threads, 1 in 4 chance that 
    - if each thread has its own dictionary, a get req will land on a random one, which give u only 3 in 4 chances that it returns the correct, the rest 404 becat the key doesn exsit on the other threads' dictionaries

sample text 
