clear_pyc:
	find . -name '*.pyc' -delete

test: clear_pyc
	env unittest=true py.test ./tests
	env unittest=true py.test ./fastgets --doctest-modules

pub: 
	python3 setup.py sdist upload
