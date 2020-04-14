##############################################################################
# transforms a flowfile to add geohash enrichment using pygeohash
#
# Variables provided in scope by script engine:
#
#    session - ProcessSession
#    context - ProcessContext
#    log - ComponentLog
#    REL_SUCCESS - Relationship
#    REL_FAILURE - Relationship
###############################################################################

import json
import sys
import traceback
from java.nio.charset import StandardCharsets
from org.apache.commons.io import IOUtils
from org.apache.nifi.processor.io import StreamCallback
from org.python.core.util import StringUtil
from h3 import h3
import pandas as pd


class TransformCallback(StreamCallback):
    def __init__(self):
        pass

    def process(self, inputStream, outputStream):
        try:
            # Read input FlowFile content
            input_text = IOUtils.toString(inputStream, StandardCharsets.UTF_8)
            input_obj = json.loads(input_text)

            # Transform content
            output_obj = input_obj
            #output_obj['value'] = output_obj['value'] * output_obj['value']
            #output_obj['message'] = 'Hello'

            h3_level=8
            output_obj['h3'] = output_obj.apply(lambda x: h3.geo_to_h3(x.lat, x.lon, h3_level), axis=1) # >>> ‘ezs42’

            # Write output content
            output_text = json.dumps(output_obj)
            outputStream.write(StringUtil.toBytes(output_text))
        except:
            traceback.print_exc(file=sys.stdout)
            raise


flowFile = session.get()
if flowFile != None:
    flowFile = session.write(flowFile, TransformCallback())

    # Finish by transferring the FlowFile to an output relationship
    session.transfer(flowFile, REL_SUCCESS)
