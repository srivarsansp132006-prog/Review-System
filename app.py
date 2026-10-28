from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

reviews = []
counter = 1

class SimpleReviewHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Build list with both Edit and Delete forms
        items_html = ""
        for r in reviews:
            items_html += f"""
            <li style="margin-bottom: 12px;">
                [ID: {r['id']}] <b>{r['author']}</b>: {r['comment']}
                <!-- Edit Review -->
                <form method="POST" action="/edit" style="display:inline; margin-left: 10px;">
                    <input type="hidden" name="id" value="{r['id']}" />
                    <input type="text" name="new_comment" placeholder="Update review..." required />
                    <button type="submit">Update</button>
                </form>
                <!-- Delete Review (v3 Feature) -->
                <form method="POST" action="/delete" style="display:inline; margin-left: 6px;">
                    <input type="hidden" name="id" value="{r['id']}" />
                    <button type="submit" style="color:red;">Delete</button>
                </form>
            </li>
            """

        if not items_html:
            items_html = "<li>No reviews yet.</li>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Review System - v3</title></head>
        <body style="font-family: Arial; padding: 25px;">
            <h2>Review System - v3</h2>
            <p><b>Features:</b> Add Review + Edit Review + Delete Review</p>
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
        global counter, reviews
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        params = urllib.parse.parse_qs(body)

        if self.path == '/add':
            author = params.get('author', [''])[0]
            comment = params.get('comment', [''])[0]
            if author and comment:
                reviews.append({'id': counter, 'author': author, 'comment': comment})
                counter += 1

        elif self.path == '/edit':
            review_id = int(params.get('id', ['0'])[0])
            new_comment = params.get('new_comment', [''])[0]
            for r in reviews:
                if r['id'] == review_id:
                    r['comment'] = new_comment
                    break

        elif self.path == '/delete':
            review_id = int(params.get('id', ['0'])[0])
            reviews = [r for r in reviews if r['id'] != review_id]

        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

def run():
    server = HTTPServer(('0.0.0.0', 3000), SimpleReviewHandler)
    print("Python server running on port 3000...")
    server.serve_forever()

if __name__ == '__main__':
    run()