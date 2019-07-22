from flask import Flask
from Format import concat
import re
import requests

app = Flask(__name__)


@app.route('/admin')
def admin():
    print('admin')
    return "admin"


@app.route('/price/<id>')
def hello(id):
    res = requests.get("https://item.taobao.com/item.htm?id=%s" % (str(id)))
    content = res.text
    a = re.findall('";(.*?);".*?e":"(\d+\.\d+).*?d":"(\d+)', content)
    j = []
    for i in range(len(a)):
        y = {"data-value": a[i][0], "price": a[i][1], "skuid": a[i][2]}
        d = y['data-value'].split(";")
        attr = []
        for l in d:
            pattern = 'data-value="' + l + '".*?\s+.*?\s+<span>(.*?)</span>'
            g = re.search(pattern, content).group(1)
            attr.append(g)
        y['attribute'] = attr
        t = concat(y, ',')
        j.append(t)
    return "<br>".join(j)


def takeSecond(elem):
    return elem[1]


# "https://item.taobao.com/item.htm?id=524223874270"
if __name__ == '__main__':
    app.run()