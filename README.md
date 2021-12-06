# Crowsnest Chart Server

Starts an instance of a `tileserver-gl` to serve a S-57 chart encoded as a MBTiles file.

## Quickstart

The binded volume must contain a MBtiles file named `chart.mbtiles`.

```
docker run -it -p 8080:8080 -v ${PWD}/tiles:/data/tiles --env TILE_SOURCE_URL_HOST='localhost:8080' crowsnest-chart-server
```

The chart and the styles in which it can be reviewd at `localhost:8080`.
