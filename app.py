from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# List to store our reviews in memory
reviews = []
counter = 1

class SimpleReviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Build list of reviews
        items_html = "".join([f"<li>[ID: {r['id']}] <b>{r['author']}</b>: {r['comment']}</li>" for r in reviews])
        if not items_html:
            items_html = "<li>No reviews yet.</li>"

        # HTML Page
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Review System - v1</title></head>
        <body style="font-family: Arial; padding: 25px;">
            <h2>Review System - v1</h2>
            <p><b>Feature:</b> Add Review</p>
            <form method="POST" action="/add">
                <input type="text" name="author" placeholder="Your Name" required /><br><br>
                <input type="text" name="comment" placeholder="Your Review" required /><br><br>
                <button type="submit">Submit Review</button>
            </form>
            <hr>
            <h3>All Reviews:</h3>
            <ul>{items_html}</ul>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        global counter
        if self.path == '/add':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            params = urllib.parse.parse_qs(body)

            author = params.get('author', [''])[0]
            comment = params.get('comment', [''])[0]

            if author and comment:
                reviews.append({'id': counter, 'author': author, 'comment': comment})
                counter += 1

            # Redirect back to home
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

def run():
    server = HTTPServer(('0.0.0.0', 3000), SimpleReviewHandler)
    print("Python server running on port 3000...")
    server.serve_forever()

if __name__ == '__main__':
    run()