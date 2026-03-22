# Interactive Map Game

## Goal
This is a game that helps people learn country names, locations, flags, and capitals.

It centres around an interactive map displaying the outlines of every country in the world. The user can zoom in and out and pan around the map. Hovering over a country highlights it and its outline.

## Stack
- **D3.js v7** (via CDN) — data-driven SVG rendering and zoom behavior
- **topojson-client** (via CDN) — decode TopoJSON (smaller format, shared borders)
- **world-atlas** TopoJSON data (jsDelivr CDN) — public domain Natural Earth data
- Vanilla HTML/CSS/JS — no build tool, no npm required

## Data Source
TopoJSON from the `topojson/world-atlas` package (Natural Earth, public domain):
```
https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json
```
~200KB (50m resolution). Encodes shared borders once, reducing file size vs GeoJSON.

## File Structure
```
index.html    — page shell, D3 + TopoJSON CDN imports, SVG container
style.css     — fullscreen layout, country fill/stroke, .highlighted class
main.js       — projection setup, SVG render, zoom behavior, hover events
```
