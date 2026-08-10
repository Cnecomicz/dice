# Changelog

All notable changes to this project are documented here.
This project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

## [1.0.0] - 2026-08-10
### Added
- Initial public release.
- Dice model (`Dice`) with validation, canonical dice-syntax serialization
    via `to_string()`, keep-highest, multiplier, summand, and per-level
    scaling.
- Usage dice (`UsageDie`, `UsageResult`) modeling resources that wear down
    along regular and Zocchi ladders, with prestige support.
- Dice-syntax codecs (`parse`, `parse_dice`, `parse_usagedie`) that generate
    `Dice`/`UsageDie` objects.
- Randomness seam (`dice_rng`) with an `Rng` protocol, `DefaultRng`, and
    a shared `default_rng()` for dependency-injectable rolling.
- Rolling API (`roll`, `RollResult`) returning full roll detail.
- Check API (`check_above`, `check_below`, `thread_the_needle`, `CheckResult`)
    with signed advantage/disadvantage and tie handling.