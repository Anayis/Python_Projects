""" Google App Engine validation form
Yuttanant Suwansiri 16 May 2013"""

import webapp2

form = """
<form method="post">
    What is your birthday?
    <br>
    <label>
        Month
        <input type="text" name="month">
    </label>
    <label>
        Day
        <input type="text" name="day">
    </label>
    <label>
        Year
        <input type="text" name="year">
    </label>
    <br><br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):

    def get(self):
       # self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(form)

class TestHandler(webapp2.RequestHandler):
    def get(self):
        q=self.request.get("q")
        self.response.out.write(q)

application = webapp2.WSGIApplication([('/', MainPage), ('/testform', TestHandler)], debug=True)
