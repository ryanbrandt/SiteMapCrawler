from flask import Flask, render_template, request, url_for, jsonify
from forms import DomainForm
from SoupCrawler import SoupCrawler
import jinja2
import os

application = Flask(__name__)
application.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


@application.route('/', methods=['GET', 'POST'])
def index():
    '''
    Index renderer/site map request handler
    :return:
        GET: Rendered index.html
        POST: JSON: generated site map (see SoupCrawler.site_map)
    '''
    if request.method == 'POST':
        sc = SoupCrawler(request.get_data('domain').decode('utf-8'))
        sc.do_crawl(sc.domain)

        return jsonify(sc.site_map)

    template = jinja_env.get_template('index.html')
    form = DomainForm()

    return render_template(template, form=form, styles_url=url_for('static', filename='main.css'), js_url=url_for('static', filename='main.js'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    application.run(host='0.0.0.0', port=port)
