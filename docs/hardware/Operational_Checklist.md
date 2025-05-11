# Operational Checklist for QartvelNest Ground Station

## Daily Operations
- Update satellite TLE data (`cron` job).
- Run `satnogs-auto-scheduler` to queue upcoming passes.

## Weekly Checks
- Visually inspect antennas and cables.
- Verify antenna SWR (<1.3).

## Post-Pass Verification
- Confirm telemetry packets stored correctly in DB (via UI).

## Emergency Protocols
- Severe weather (>50 kA lightning forecast): disconnect antenna feedlines immediately.

## Maintenance Logs
- Record any issues, maintenance performed, or software updates in this repository's issue tracker for clear documentation.
