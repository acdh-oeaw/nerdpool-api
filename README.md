[![Test, Build, Release](https://github.com/acdh-oeaw/nerdpool/actions/workflows/build.yml/badge.svg)](https://github.com/acdh-oeaw/nerdpool/actions/workflows/build.yml)

# nerdpool

a simple django web application to publish Named Entity Training Data. Please see https://digital-humanities.at/en/dha/s-project/nerdpool-data-pool-named-entity-recognition


## install

* clone the repo `git clone https://github.com/acdh-oeaw/nerdpool.git`
* cd into the repo `cd nerdpool`
* optional but recommended: create a virtuale environment e.g. `virtualenv env`
* install requirements (if you don't need postgres, install requirement_dev.txt) `pip install requirements_dev.txt`
* run migration `python manage.py migrate`

### import datasets

run the import scripts:

* `python manage.py import_RTA`
* `python manage.py import_RITA`
* `python manage.py import_ALED`
* `python manage.py import_MRP`
* `python manage.py import_DIPKO`

(if you run on sqllite, this might take a while, but for simple testing, just interrupt the import script (ctrl+d))

## docker

### build

`docker build -t np:latest .`

### run and import data
`docker run -e IMPORTDATA -it -p 8020:8020  np:latest`
