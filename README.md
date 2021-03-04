# Point Cloud Extension

- **Title:** Point Cloud
- **Identifier:** <https://stac-extensions.github.io/pointcloud/v1.0.0/schema.json>
- **Field Name Prefix:** pc
- **Scope:** Item, Collection
- **Extension [Maturity Classification](https://github.com/radiantearth/stac-spec/tree/master/extensions/README.md#extension-maturity):** Proposal
- **Owner**: @matthewhanson
- **History**: [Prior to March 2nd, 2021](https://github.com/radiantearth/stac-spec/tree/3a83d75aec7f16ae597ee9779777a97e83ff46a4/extensions/pointcloud)

This document explains the Point Cloud Extension to the [SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec) (STAC)
specification. It adds fields to a STAC Item, to enable STAC to more fully describe point cloud datasets. The
point clouds can come from either active or passive sensors, and data is frequently acquired using tools such as LiDAR or coincidence-matched imagery.

- Examples:
  - [Example](examples/example-autzen.json)
- [JSON Schema](json-schema/schema.json)

## Item Properties fields

| Field Name    | Type                              | Description |
| ------------- | --------------------------------- | ----------- |
| pc:count      | integer                           | **REQUIRED.** The number of points in the Item. |
| pc:type       | string                            | **REQUIRED.** Phenomenology type for the point cloud. Possible valid values might include `lidar`, `eopc`, `radar`, `sonar`, or `other` |
| pc:encoding   | string                            | **REQUIRED.** Content encoding or format of the data. |
| pc:schemas    | [[Schema Object](#schema-object)] | **REQUIRED.** A sequential array of Items that define the dimensions and their types. |
| pc:density    | number                            | Number of points per square unit area. |
| pc:statistics | [[Stats Object](#stats-object)]   | A sequential array of Items mapping to `pc:schemas` defines per-channel statistics. |

### Schema Object

A sequential array of Items that define the dimensions or channels of
the point cloud, their types, and their sizes (in full bytes).

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

## Implementations

None yet, still in proposal stage.
