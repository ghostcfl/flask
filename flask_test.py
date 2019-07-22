from flask import Flask, render_template, request
import requests, re
from Format import concat

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # result = request.form
        result = request.form
        item = result.to_dict()
        itemID = item['itemID']
        res = requests.get("https://item.taobao.com/item.htm?id=%s" % (str(itemID)))
        content = res.text
        print(content)
        # a = re.findall('";(.*?);".*?e":"(\d+\.\d+).*?d":"(\d+)', content)
        a = re.findall('";(.*?);".*?e":"(\d+\.\d+)', content)
        if a:
            j = []
            for i in range(len(a)):
                # y = {"data-value": a[i][0], "price": a[i][1], "skuid": a[i][2]}
                y = {"data-value": a[i][0], "price": a[i][1]}
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
        else:
            print("c")
            print(content)
            k = "".join(re.findall('<input.*?name="current.*?"(\d+\.\d+)', content))
            print(k)
            return "price=" + k


if __name__ == '__main__':
    app.run()
