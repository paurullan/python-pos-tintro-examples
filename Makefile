all: uptime
P=docker-compose run --rm python
uptime:
	docker-compose run --rm python counter-corrutine.py

scraper:
	docker-compose run --rm python mobile-status-scrap.py

chain:
	$P chain.py

queue:
	$P test_queue.py

shell:
	docker-compose run --rm python

pylint:
	# entrypoint params go before «python» image
	docker-compose run --rm --entrypoint pylint python mobile-status-scrap.py

