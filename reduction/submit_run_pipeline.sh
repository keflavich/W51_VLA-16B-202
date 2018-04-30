#!/bin/bash

OBSDATE=$1
sed s/REPLACETHIS/${OBSDATE}/ req_pipeline.req > req_pipeline_${OBSDATE}.req
submit -f req_pipeline_${OBSDATE}.req
