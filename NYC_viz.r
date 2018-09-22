library(rgeos)
library(maptools)
library(geojsonio)
library(ggplot2)
library(viridis)


URLz <- "http://data.beta.nyc//dataset/3bf5fb73-edb5-4b05-bb29-7c95f4a727fc/resource/6df127b1-6d04-4bb7-b983-07402a2c3f90/download/f4129d9aa6dd4281bc98d0f701629b76nyczipcodetabulationareas.geojson"
filz <- "nyc_community_zip.geojson"
download.file(URLz, filz)

nyc_zips <- geojson_read(filz, what="sp")
nyc_zips_map <- fortify(nyc_zips, region="postalCode")

set.seed(1492)
c2 <- read.csv("temp.csv")
gg <- ggplot()
gg <- gg + geom_map(data=nyc_zips_map, map=nyc_zips_map,
                    aes(x=long, y=lat, map_id=id),
                    color="#2b2b2b", size=0.15, fill=NA)
gg <- gg + geom_map(data=c2, map=nyc_zips_map,
                    aes(fill=fill2, map_id=zip),
                    color="#2b2b2b", size=0.15)
gg <- gg + scale_fill_viridis(name="Better title\nthan 'fill'")
gg <- gg + coord_map()
gg <- gg + ggthemes::theme_map()
gg <- gg + theme(legend.position=c(0.1,0.5))
gg
