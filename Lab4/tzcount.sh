#!/bin/bash
git log "$@" --pretty=format:"%ci" | awk '{print $3}' | sort -g | uniq -c | awk '{print $2" "$1}'
