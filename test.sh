#!/usr/bin/env bash

./.venv/bin/coverage run -m unittest discover src
./.venv/bin/coverage html
