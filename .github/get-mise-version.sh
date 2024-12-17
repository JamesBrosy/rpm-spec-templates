#!/bin/bash

curl -s https://api.github.com/repos/jdx/mise/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")' | tr -d 'v'
