#!/bin/bash

curl -s https://api.github.com/repos/$1/$2/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")'
