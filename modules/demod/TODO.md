# Demod Module — Milestones

| Status |   #   | Commit Tag        | Goal                          | Testable Result                                          |
| :----: | :---: | ----------------- | ----------------------------- | -------------------------------------------------------- |
|   ⬜️   | **0** | `demod-scaffold`  | Package skeleton + tox config | `pytest -q` runs zero tests, exits 0.                    |
|   ⬜️   | **1** | `crc16`           | CRC‑16/CCITT function + tests | Matches reference vectors from AMSAT docs.               |
|   ⬜️   | **2** | `ax25-frame-sync` | Bit‑unstuff + flag detection  | Unit test decodes frame in `sample.ax25`; FCS verified.  |
|   ⬜️   | **3** | `zmq-publisher`   | ZeroMQ PUB on `tcp://*:5557`  | Subscriber script receives JSON payload; CI test passes. |
|   ⬜️   | **4** | `bench-100fps`    | Real‑time decode benchmark    | 10‑minute file processed < 600 ms on RPi 4 in CI.        |
