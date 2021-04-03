#!/bin/bash
docker run -td --name dash --env-file ./env.list -p 80:3000 dash-img:latest