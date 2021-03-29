# nerdpool

a simple django web application to publish Named Entity Training Data. Please see https://digital-humanities.at/en/dha/s-project/nerdpool-data-pool-named-entity-recognition

## docker

### build

`docker build -t np:latest .`

### run and import data
`docker run -e IMPORTDATA -it -p 8020:8020  np:latest`
