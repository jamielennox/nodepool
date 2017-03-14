# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import signal
import sys

import nodepool.cmd
import nodepool.nodepool
import nodepool.webapp


class NodePoolWebApp(nodepool.cmd.NodepoolDaemonApp):

    app_name = 'webapp'
    app_description = 'Web reponder for nodepool information'

    def __init__(self):
        super(NodePoolWebApp, self).__init__()
        self.webapp = None

    def create_parser(self):
        parser = super(NodePoolWebApp, self).create_parser()

        parser.add_argument('-c', dest='config',
                            default='/etc/nodepool/nodepool.yaml',
                            help='path to config file')
        parser.add_argument('-s', dest='secure',
                            default='/etc/nodepool/secure.conf',
                            help='path to secure file')

        return parser

    def exit_handler(self, signum, frame):
        self.webapp.stop()
        sys.exit(0)

    def term_handler(self, signum, frame):
        os._exit(0)

    def run(self):
        pool = nodepool.nodepool.NodePool(self.args.secure, self.args.config)
        self.webapp = nodepool.webapp.WebApp(pool)

        signal.signal(signal.SIGTERM, self.term_handler)
        signal.signal(signal.SIGINT, self.exit_handler)

        self.webapp.start()

        while True:
            signal.pause()


def main():
    return NodePoolWebApp.main()


if __name__ == "__main__":
    sys.exit(main())
