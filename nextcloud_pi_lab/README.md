# Nextcloud isolated ARM64: Supervisor startup laboratory

**Not a family-cloud release. Do not add real data.**

- Separate add-on slug `nextcloud_isolated_pi_lab`, independent of Maison Hub Lab.
- `/data` is a Supervisor-managed app volume. No bind mounts or host file access.
- Manual boot, no host ports, no Ingress, no privileged access or HA API credentials.
- This build only exercises container initialization and restart behavior on a real ARM64 HA OS machine; there is deliberately no browser access.
- Does not install automatically. Run a safety review and an image build test in GitHub Actions first.
- Remaining release blockers: real Supervisor runtime, Ingress subpath handling, SQLite-to-supported-database strategy, secrets, upgrades, rollback, and a native backup/restore rehearsal.
- The official upstream tag must be replaced with a tested immutable digest before deployment beyond the isolated lab.
