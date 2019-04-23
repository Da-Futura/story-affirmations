#!/bin/bash
exec parcel watch src/ui/index.html &
./bin/run_api.sh

