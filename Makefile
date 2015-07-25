all:
	docker-compose run --rm python mobile-status-scrap.py

shell:
	docker-compose run --rm python

pylint:
	# entrypoint params go before «python» image
	docker-compose run --rm --entrypoint pylint python mobile-status-scrap.py

