# Uplink Module — Milestones

| Status |   #   | Commit Tag        | Goal                                         | Testable Result                                                      |
| :----: | :---: | ----------------- | -------------------------------------------- | -------------------------------------------------------------------- |
|   ⬜️   | **0** | `uplink-scaffold` | FastAPI service skeleton on port 4600        | `curl /docs` opens OpenAPI page; pytest zero tests passes.           |
|   ⬜️   | **1** | `packetizer`      | Build AX.25 UI frame w/ CRC                  | Unit test compares to golden hex frame.                              |
|   ⬜️   | **2** | `wav-generator`   | NumPy Bell202 AFSK `.wav` generator          | FFT shows peaks at 1200/2200 Hz; round‑trip with multimon‑ng passes. |
|   ⬜️   | **3** | `zmq-publish`     | Push raw bytes to `tcp://*:5566` in sim mode | Integration test: simulator receives frame and ACKs.                 |
|   ⬜️   | **4** | `cli-tool`        | `send_cmd.py` one‑off command sender         | `python send_cmd.py 0x10 5` writes `.wav` file and logs path.        |
