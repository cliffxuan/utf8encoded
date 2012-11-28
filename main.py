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
        html = '<html>'\
                    '<body>'\
                        '<strong>Convert text file to utf-8 encoded text file.</strong>'\
                        '<form action="" method="post" enctype="multipart/form-data">'\
                            '<input type="file" name="textfile">'\
                            '<input type="submit" name="Upload">'\
                        '</form>'\
                    '</body>'\
                '<html/>'
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(html)

    def post(self):
        environ = self.request.environ
        fs = cgi.FieldStorage(fp=environ['wsgi.input'],environ=environ)['textfile']
        file_name = fs.filename
        if file_name:
            try:
                raw_file_utf_8 = make_sure_utf_8(fs.file.read())
            except UnSupportedEncoding, e:
                self.response.code = 400
                self.response.headers['Content-Type'] = 'text/html'
                self.response.out.write(e)
            else:
                new_file_name = modify_file_name(file_name)
                self.response.headers['Content-Type'] = 'text/plain'
                self.response.headers['Content-Disposition'] = 'attachment; filename=%s' %new_file_name
                self.response.out.write(raw_file_utf_8)
        else:
            html = '<html>'\
                        '<body>'\
                            '<p style="color:red;">File empty</p>'\
                            '<strong>Convert text file to utf-8 encoded text file.</strong>'\
                            '<form action="" method="post" enctype="multipart/form-data">'\
                                '<input type="file" name="textfile">'\
                                '<input type="submit" name="Upload">'\
                            '</form>'\
                        '</body>'\
                    '<html/>'
            self.response.headers['Content-Type'] = 'text/html'
            self.response.write(html)
            

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
