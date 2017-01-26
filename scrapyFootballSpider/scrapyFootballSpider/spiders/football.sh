#! /bin/bash
# first, store main page title
# second, store main page all image url like http://img.dongqiudi.com/data
# then, from main page, store all title and url recursively
# site: www.dongqiudi.com
scrapy crawl footballTitle -o football.csv -t csv -s LOG_FILE=football.log
scrapy crawl footballImage -o football.csv -t csv -s LOG_FILE=football.log
scrapy crawl footballUrl   -o football.csv -t csv -s LOG_FILE=football.log


