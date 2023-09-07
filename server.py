# This is a simple test server for use with the Well-Architected labs
# It simulates an engine for recommending TV shows
#
# This code is only for use in Well-Architected labs
# *** NOT FOR PRODUCTION USE ***
#
#
# Licensed under the Apache 2.0 and MITnoAttr License.
#
# Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
# https://aws.amazon.com/apache2.0/

from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from ec2_metadata import ec2_metadata
import sys
import getopt
import boto3
import traceback
import random

__author__    = "Seth Eliot"
__email__     = "seliot@amazon.com"
__copyright__ = "Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved."
__credits__   = ["Seth Eliot", "Adrian Hornsby"]

# html code template for the default page served by this server
html = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{Title}</title>
        <link rel="icon" type="image/ico" href="https://a0.awsstatic.com/main/images/site/fav/favicon.ico" />
    </head>
    <body>
        <p>{Content}</p>
    </body>
</html>"""

# RequestHandler: Response depends on type of request made
class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, region, *args, **kwargs):
        self.region = region
        super().__init__(*args, **kwargs)

    def do_GET(self):
        print("path: ", self.path)

        # Default request URL without additional path info (main response page)
        if self.path == '/':

            # Return a success status code
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            message = "<h1>Success</h1>"

            # Add metadata
            message += get_metadata()

            self.wfile.write(
                bytes(
                    html.format(Title="healthcheck", Content=message),
                    "utf-8"
                )
            )

        return
    
# Retrieve Metadata which can be useful to students 
# For example to see which instance /  AWS AZ they are hitting
def get_metadata():
    metadata = '<br/><hr><h3>EC2 Metadata</h3>'
    try:
        message_parts = [
            'account_id: %s' % ec2_metadata.account_id,
            'ami_id: %s' % ec2_metadata.ami_id,
            'availability_zone: %s' % ec2_metadata.availability_zone,
            'instance_id: %s' % ec2_metadata.instance_id,
            'instance_type: %s' % ec2_metadata.instance_type,
            'private_hostname: %s' % ec2_metadata.private_hostname,
            'private_ipv4: %s' % ec2_metadata.private_ipv4
        ]
        metadata += '<br>'.join(message_parts)
    except Exception:
        metadata += "Running outside AWS"

    return metadata

# Initialize server
def run(argv):
    try:
        opts, args = getopt.getopt(
            argv,
            "hs:p:r:",
            [
                "help",
                "server_ip=",
                "server_port=",
                "region="
            ]
        )
    except getopt.GetoptError:
        print('server.py -s <server_ip> -p <server_port> -r <AWS region>')
        sys.exit(2)
    print(opts)

    # Default value - will be over-written if supplied via args
    server_port = 80
    server_ip = '0.0.0.0'
    try:
        region = ec2_metadata.region
    except:
        region = 'us-east-2'

    # Get commandline arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('server.py -s <server_ip> -p <server_port> -r <AWS region>')
            sys.exit()
        elif opt in ("-s", "--server_ip"):
            server_ip = arg
        elif opt in ("-p", "--server_port"):
            server_port = int(arg)
        elif opt in ("-r", "--region"):
            region = arg

    # start server
    print('starting server...')
    server_address = (server_ip, server_port)

    handler = partial(RequestHandler, region)
    httpd = HTTPServer(server_address, handler)
    print('running server...')
    httpd.serve_forever()


if __name__ == "__main__":
    run(sys.argv[1:])