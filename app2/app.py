from flask import Flask, render_template_string
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
  <h1>DevOpsHub Dashboard</h1>
  <p>Total visits to App 1: {{ visits }}</p>
  <p>Total messages collected: {{ count }}</p>
  <h2>All Messages:</h2>
  <ul>
    {% for msg in messages %}
      <li>{{ msg }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""

@app.route('/')
def dashboard():
    count = r.llen('messages')
    visits = r.get('visits')
    visits = visits.decode() if visits else '0'
    messages = [m.decode() for m in r.lrange('messages', 0, -1)]
    return render_template_string(HTML, count=count, visits=visits, messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    #abbe finished and about to psuh