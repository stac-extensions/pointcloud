# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [v2.0.0] - 2024-08-21

### Changed

- Updated to "Pilot" maturity
- Required properties of type `string` require a minimum length of `1`
- `pc:schemas` is no longer required

### Removed

- `pc:encoding` because there is an encoding key in the asset

### Fixed

- Fixed JSON Schema, which allowed pointcloud fields in the top-level of Collections

## [v1.0.0] - 2021-03-08

Initial independent release, see [previous history](https://github.com/radiantearth/stac-spec/commits/v1.0.0-rc.1/extensions/pointcloud)

[Unreleased]: <https://github.com/stac-extensions/pointcloud/compare/v2.0.0...HEAD>
[v2.0.0]: <https://github.com/stac-extensions/pointcloud/compare/v1.0.0...v2.0.0>
[v1.0.0]: <https://github.com/stac-extensions/pointcloud/tree/v1.0.0>
