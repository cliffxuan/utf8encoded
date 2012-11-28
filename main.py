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
import os
import cgi
import webapp2
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),
        'templates')))

class UnSupportedEncoding(Exception):
    pass

def make_sure_utf_8(text):
    """make sure the text is encoded in utf-8"""
    attempt_charsets = ['utf-8', 'latin-1']
    for charset in attempt_charsets:
        try:
            return text.decode(charset).encode('utf-8')
        except UnicodeDecodeError:
            continue
    else:
        raise UnSupportedEncoding('The file encoding is not supported.')

def modify_file_name(file_name):
    pos = file_name.rfind('.')
    if pos == -1:
        return file_name + '-utf8'
    else:
        return file_name[:pos] + '-utf8' + file_name[pos:]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render({}))

    def post(self):
        environ = self.request.environ
        fs = cgi.FieldStorage(fp=environ['wsgi.input'],environ=environ)['textfile']
        file_name = fs.filename
        template = jinja_environment.get_template('index.html')
        if file_name:
            try:
                raw_file_utf_8 = make_sure_utf_8(fs.file.read())
            except UnSupportedEncoding, e:
                self.response.code = 400
                self.response.headers['Content-Type'] = 'text/html'
                self.response.write(e)
            else:
                new_file_name = modify_file_name(file_name)
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.headers['Content-Disposition'] = 'attachment; filename=%s' %new_file_name
                self.response.write(raw_file_utf_8)
        else:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(template.render({'error':'choose a file'}))
            

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
