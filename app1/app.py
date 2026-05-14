from flask import Flask, request, render_template_string
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Message Collector</title></head>
<body>
  <h1>DevOpsHub Feedback</h1>
  <p>Visit count: {{ visits }}</p>
  <form method="POST">
    <input type="text" name="message" placeholder="Your message" required>
    <button type="submit">Send</button>
  </form>
  <p>Messages collected: {{ count }}</p>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    r.incr('visits')
    if request.method == 'POST':
        msg = request.form['message']
        r.rpush('messages', msg)
    visits = r.get('visits').decode()
    count = r.llen('messages')
    return render_template_string(HTML, visits=visits, count=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)