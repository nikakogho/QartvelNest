# Downlink Module — Milestones

| Status |   #   | Commit Tag          | Goal                                                    | Testable Result                                                     |
| :----: | :---: | ------------------- | ------------------------------------------------------- | ------------------------------------------------------------------- |
|   ⬜️   | **0** | `downlink-scaffold` | **Env & CLI skeleton**                                  | `python run_downlink.py --help` prints usage.                       |
|   ⬜️   | **1** | `fifo-writer`       | FIFO at `/tmp/qartvelsat/downlink.bits` writes 0x55 pattern | Reading FIFO shows repeating bytes; unit test passes.               |
|   ⬜️   | **2** | `mock-sdr-input`    | File-source IQ → bits                                   | Unit test feeds `test.iq` → FIFO length > 1 kbit.                   |
|   ⬜️   | **3** | `rtl-live-mode`     | RTL-SDR live capture demo                               | FIFO fills with bits when tuned to FM broadcast; manual demo video. |
|   ⬜️   | **4** | `docs-config`       | README & `config/downlink.yml` schema                   | `pydantic` validation unit test; README explains flags.             |
