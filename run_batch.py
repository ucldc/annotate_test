#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" facet decade in python """

import sys
import argparse
import re
from datetime import date
import itertools
import json

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from pprint import pprint as pp

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('md5s')

    if argv is None:
        argv = parser.parse_args()

    with open(argv.md5s) as file:
        for line in file:
            md5 = line.rstrip('\n')
            data = get_640(md5)
            with open('{}.json'.format(md5), 'w') as f:
                json.dump(
                    data, f, ensure_ascii=False, sort_keys=True)


def get_640(md5):
    credentials = GoogleCredentials.get_application_default()
    client = discovery.build(
        'vision',
        'v1',
        credentials=credentials,
        discoveryServiceUrl=DISCOVERY_URL)

    batch_request = []

    batch_request.append({
        "features": [{
            "type": "LANDMARK_DETECTION"
        }, {
            "type": "LABEL_DETECTION"
        }, {
            "type": "SAFE_SEARCH_DETECTION"
        }, {
            "type": "TEXT_DETECTION"
        }, {
            "type": "FACE_DETECTION"
        }, {
            "type": "LOGO_DETECTION"
        }],
        "image": {
            "source": {
                "gcsImageUri":
                "gs://calisphere-images/100-640x480/{}-640x480.jpg".format(md5)
            }
        }
    })

    request = client.images().annotate(body={'requests': batch_request})
    response = request.execute(num_retries=3)
    return response

# main() idiom for importing into REPL for debugging
if __name__ == "__main__":
    sys.exit(main())
"""
Copyright © 2016, Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the University of California nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
