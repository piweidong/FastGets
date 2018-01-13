clear_pyc:
	find . -name '*.pyc' -delete

test: clear_pyc
	env unittest=true py.test ./fastgets --doctest-modules


