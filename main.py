import pdb
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi

import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        html = '<html>'\
                    '<body>'\
                        '<form action="#" method="post">'\
                            '<input type="file" name="file">'\
                            '<input type="submit" name="Upload">'\
                        '</form>'\
                    '</body>'\
                '<html/>'
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)

    def post(self):
        fileitem = self.request.get('file')
        pdb.set_trace() ############################## Breakpoint ##############################
        self.response.out.write(cgi.escape(fileitem))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)