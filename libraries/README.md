# Visualizer Libraries

This directory is the library/catalog layer for the visualizer assets currently present in the repository.

## Inventory

| File | Type | Size | Library role |
|---|---|---:|---|
| `../ave.txt` | Documentation | 16,378 B | Element/property reference for the visualizer engine |
| `../sample.viz` | Visualizer asset | 164,621 B | Sample `.viz` visualizer definition |
| `../scene.json` | Scene definition | 721,277 B | Large visualizer scene/library source |
| `../scene1.json` | Scene definition | 252,733 B | Visualizer scene/library source |
| `../scene2.json` | Scene definition | 207,169 B | Visualizer scene/library source |
| `../scene3.json` | Scene definition | 419,348 B | Visualizer scene/library source |

## Classification

### Core element/property documentation
`ave.txt` documents Text, Segments/Bars, Composition, Particles, Image, Audio Provider (including Spectrum and Waveform), and visual effects such as Blur, RGB Split, Motion Blur, and Mirror. It should be treated as the reference catalog for element names and properties rather than as executable visualizer content.

### Visualizer definitions
`sample.viz` and the four `scene*.json` files are content assets. They should be preserved byte-for-byte when imported into the visualizer library because their JSON/VIZ structure is part of the source-of-truth data.

## Important handling rule

The original files remain in the repository root so existing paths are not broken. This `libraries` directory is the organized library/catalog entry point; it references the originals instead of duplicating or rewriting large visualizer files.

## Current count

**6 source files** are registered in the library catalog: **1 documentation file + 1 `.viz` asset + 4 JSON scene assets**.
