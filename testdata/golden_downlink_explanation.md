# What's inside

| Section           | Bytes (hex)              | Notes                                                         |
| ----------------- | ------------------------ | ------------------------------------------------------------- |
| Flag              | **7E**                   | Start of AX.25 frame                                          |
| Dest “SAT1  ”     | A6 82 A8 62 40 40 60     | Callsign chars shifted <<1, SSID 0, ext=0                     |
| Src  “NEST  ”     | 9C 8A A6 A8 40 40 **61** | SSID 0, **ext=1** (last address)                              |
| Control / PID     | **03 F0**                | UI frame, no layer-3                                          |
| Telemetry payload | **01 3C 00 B8 0B 1E 05** | PacketID=1, uptime=60 s, batt=3000 mV, temp=30 °C, beacon=5 s |
| CRC-16 (payload)  | **FA 99**                | CCITT over 7-byte payload (little-endian)                     |
| Frame FCS         | **5A 1F**                | AX.25 X25 CRC (little-endian)                                 |
| Flag              | **7E**                   | End flag                                                      |
