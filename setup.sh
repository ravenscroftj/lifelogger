#!/bin/sh

make bootstrap

rm -rf lifelog/static/bootstrap
mv bootstrap lifelog/static
