# python-pos-tintro-examples

Python snippets and examples beyond your simpler tutorials; like «Python 201»

To make things easier this project has a little Dockerfile and docker-compose
to manage Python 3.5, because it is in beta and it would be a pain to install
in your machine. We are that awesome.

## Pre-running

apt-transport-https
http://blog.docker.com/2015/07/new-apt-and-yum-repos/
$ apt-get install docker-engine docker-compose
docker-compose --version # >= 1.3.1
docker --version # >= 1.7.1

Check also having make.

The make will directly pull the dockers (around 100MB).

:: 
# to get an interpreter
docker-compose run --rm python 


::
  make


## Links

Fast scraping in python with asyncio

http://compiletoi.net/fast-scraping-in-python-with-asyncio.html

async+wait keywords
https://www.python.org/dev/peps/pep-0492/

