#!/usr/bin/env python3
"""Generate enlarged circular click targets for small countries.

Reads countries.json for area data and the world-atlas TopoJSON for
centroids, then outputs a GeoJSON FeatureCollection of circles.

Usage:
    python3 create_small_target_map.py --radius 50 --max_area 500
"""

import argparse
import json
import math
import sys
import urllib.request


TOPOJSON_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json"
EARTH_RADIUS_KM = 6371


def load_topojson():
    """Fetch and parse the world-atlas TopoJSON."""
    with urllib.request.urlopen(TOPOJSON_URL) as resp:
        return json.loads(resp.read())


def topojson_to_geojson(topology):
    """Convert TopoJSON geometries to GeoJSON features (minimal implementation)."""
    arcs = topology["arcs"]
    transform = topology.get("transform")

    def decode_arc(arc_index):
        reverse = arc_index < 0
        idx = ~arc_index if reverse else arc_index
        arc = arcs[idx]
        coords = []
        x, y = 0, 0
        for dx, dy in arc:
            x += dx
            y += dy
            if transform:
                coords.append([
                    x * transform["scale"][0] + transform["translate"][0],
                    y * transform["scale"][1] + transform["translate"][1],
                ])
            else:
                coords.append([x, y])
        if reverse:
            coords.reverse()
        return coords

    def decode_rings(ring_indices):
        coords = []
        for idx in ring_indices:
            arc_coords = decode_arc(idx)
            if coords:
                coords.extend(arc_coords[1:])
            else:
                coords.extend(arc_coords)
        return coords

    features = []
    for geom in topology["objects"]["countries"]["geometries"]:
        gid = str(geom.get("id", "")).zfill(3)
        geom_type = geom["type"]
        if geom_type == "Polygon":
            coordinates = [decode_rings(ring) for ring in geom["arcs"]]
            features.append({
                "id": gid,
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": coordinates},
                "properties": geom.get("properties", {}),
            })
        elif geom_type == "MultiPolygon":
            coordinates = [
                [decode_rings(ring) for ring in polygon]
                for polygon in geom["arcs"]
            ]
            features.append({
                "id": gid,
                "type": "Feature",
                "geometry": {"type": "MultiPolygon", "coordinates": coordinates},
                "properties": geom.get("properties", {}),
            })
    return features


def compute_centroid(feature):
    """Compute a simple centroid (average of all coordinates)."""
    coords = feature["geometry"]["coordinates"]
    geom_type = feature["geometry"]["type"]

    all_points = []
    if geom_type == "Polygon":
        for ring in coords:
            all_points.extend(ring)
    elif geom_type == "MultiPolygon":
        for polygon in coords:
            for ring in polygon:
                all_points.extend(ring)

    if not all_points:
        return None

    lon = sum(p[0] for p in all_points) / len(all_points)
    lat = sum(p[1] for p in all_points) / len(all_points)
    return [lon, lat]


def create_circle(center, radius_km, num_points=64):
    """Create a GeoJSON polygon circle around a center point.

    Args:
        center: [longitude, latitude] in degrees
        radius_km: radius in kilometers
        num_points: number of points on the circle
    """
    lon0, lat0 = math.radians(center[0]), math.radians(center[1])
    angular_radius = radius_km / EARTH_RADIUS_KM

    coords = []
    for i in range(num_points + 1):
        bearing = 2 * math.pi * i / num_points
        lat = math.asin(
            math.sin(lat0) * math.cos(angular_radius)
            + math.cos(lat0) * math.sin(angular_radius) * math.cos(bearing)
        )
        lon = lon0 + math.atan2(
            math.sin(bearing) * math.sin(angular_radius) * math.cos(lat0),
            math.cos(angular_radius) - math.sin(lat0) * math.sin(lat),
        )
        coords.append([round(math.degrees(lon), 6), round(math.degrees(lat), 6)])

    return {"type": "Polygon", "coordinates": [coords]}


def main():
    parser = argparse.ArgumentParser(
        description="Generate enlarged click targets for small countries"
    )
    parser.add_argument(
        "--radius", type=float, default=50,
        help="Circle radius in km (default: 50)"
    )
    parser.add_argument(
        "--max_area", type=float, default=500,
        help="Maximum country area in km² to include (default: 500)"
    )
    parser.add_argument(
        "--output", type=str, default="small_targets.json",
        help="Output file path (default: small_targets.json)"
    )
    args = parser.parse_args()

    # Load country metadata
    with open("countries.json") as f:
        countries = json.load(f)

    # Find small countries
    small_ids = {
        cid for cid, data in countries.items()
        if data.get("area_km2", float("inf")) < args.max_area
    }

    if not small_ids:
        print(f"No countries with area < {args.max_area} km²")
        sys.exit(0)

    print(f"Found {len(small_ids)} countries under {args.max_area} km²")

    # Load TopoJSON and convert
    print("Fetching TopoJSON...")
    topology = load_topojson()
    geo_features = topojson_to_geojson(topology)

    # Build circle features
    circles = []
    for feature in geo_features:
        fid = feature["id"]
        if fid not in small_ids:
            continue

        centroid = compute_centroid(feature)
        if not centroid:
            print(f"  WARNING: could not compute centroid for {fid}")
            continue

        name = countries[fid]["name"]
        circle_geom = create_circle(centroid, args.radius)
        circles.append({
            "type": "Feature",
            "geometry": circle_geom,
            "properties": {
                "id": fid,
                "name": name,
                "radius_km": args.radius,
            },
        })
        print(f"  {fid}: {name} — centroid [{centroid[0]:.2f}, {centroid[1]:.2f}]")

    # Countries in countries.json but missing from TopoJSON
    found_ids = {c["properties"]["id"] for c in circles}
    missing = small_ids - found_ids
    for mid in sorted(missing):
        print(f"  WARNING: {mid} ({countries[mid]['name']}) not found in TopoJSON — skipped")

    collection = {"type": "FeatureCollection", "features": circles}

    with open(args.output, "w") as f:
        json.dump(collection, f, indent=2)

    print(f"\nWrote {len(circles)} circle features to {args.output}")


if __name__ == "__main__":
    main()
