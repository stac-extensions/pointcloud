# Point Cloud Extension Specification

- **Title:** Point Cloud
- **Identifier:** <https://stac-extensions.github.io/pointcloud/v1.0.0/schema.json>
- **Field Name Prefix:** pc
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Pilot
- **Owner**: @matthewhanson
- **History**: [Prior to March 2, 2021](https://github.com/radiantearth/stac-spec/commits/v1.0.0-rc.1/extensions/pointcloud)

This document explains the Point Cloud Extension to the [SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec)
(STAC) specification. It adds fields to a STAC Item, to enable STAC to more fully describe point cloud datasets.
The point clouds can come from either active or passive sensors, and data is frequently acquired using tools such as
LiDAR or coincidence-matched imagery.

- Examples:
  - [Example](examples/example-autzen.json)
  - [PDAL to STAC Python script](examples/pdal-to-stac.py)
  - [Environment](examples/environment.yml)
- [JSON Schema](json-schema/schema.json)
- [Changelog](./CHANGELOG.md)

## Item Properties

| Field Name    | Type                              | Description |
| ------------- | --------------------------------- | ----------- |
| pc:count      | integer                           | **REQUIRED.** The number of points in the Item. |
| pc:type       | string                            | **REQUIRED.** Phenomenology type for the point cloud. Possible valid values might include `lidar`, `eopc`, `radar`, `sonar`, or `other` |
| pc:schemas    | \[[Schema Object](#schema-object)\] | A sequential array of Items that define the dimensions and their types. |
| pc:density    | number                            | Number of points per square unit area. |
| pc:statistics | \[[Stats Object](#stats-object)\]   | A sequential array of Items mapping to `pc:schemas` defines per-channel statistics. |

### Schema Object

A sequential array of Items that define the dimensions or channels of
the point cloud, their types, and their sizes (in full **bytes**).

| Field Name | Type    | Description |
| ---------- | ------- | -------------------------- |
| name       | string  | **REQUIRED.** The name of the dimension. |
| size       | integer | **REQUIRED.** The size of the dimension in bytes. Whole bytes only are supported. |
| type       | string  | **REQUIRED.** Dimension type. Valid values are `floating`, `unsigned`, and `signed` |

### Stats Object

A sequential array of Items mapping to `pc:schemas` defines per-channel statistics. The channel name is required and at least one statistic.

| Field Name | Type    | Description |
| ---------- | ------- | ----------- |
| name       | string  | **REQUIRED.** The name of the channel. |
| position   | integer | Position of the channel in the schema. |
| average    | number  | The average of the channel. |
| count      | integer | The number of elements in the channel. |
| maximum    | number  | The maximum value of the channel. |
| minimum    | number  | The minimum value of the channel. |
| stddev     | number  | The standard deviation of the channel. |
| variance   | number  | The variance of the channel. |

## Contributing

All contributions are subject to the
[STAC Specification Code of Conduct](https://github.com/radiantearth/stac-spec/blob/master/CODE_OF_CONDUCT.md).
For contributions, please follow the
[STAC specification contributing guide](https://github.com/radiantearth/stac-spec/blob/master/CONTRIBUTING.md) Instructions
for running tests are copied here for convenience.

### Running tests

The same checks that run as checks on PR's are part of the repository and can be run locally to verify that changes are valid.
To run tests locally, you'll need `npm`, which is a standard part of any [node.js installation](https://nodejs.org/en/download/).

First you'll need to install everything with npm once. Just navigate to the root of this repository and on
your command line run:

```bash
npm install
```

Then to check markdown formatting and test the examples against the JSON schema, you can run:

```bash
npm test
```

This will spit out the same texts that you see online, and you can then go and fix your markdown or examples.

If the tests reveal formatting problems with the examples, you can fix them with:

```bash
npm run format-examples
```
