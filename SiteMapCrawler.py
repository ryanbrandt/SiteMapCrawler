from flask import Flask, render_template, request, url_for, jsonify
from forms import DomainForm
from SoupCrawler import SoupCrawler
import jinja2
import os

application = Flask(__name__)
application.config.update(dict(
    SECRET_KEY=os.environ['SUPER_SECRET_SECRET_KEY'],
    WTF_CSRF_SECRET_KEY=os.environ['SUPER_SECRET_CSRF_SECRET_KEY']
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
        sc = SoupCrawler(request.json['domain'])
        # call appropriate method based on algorithm
        if request.json['algorithm'] == 'df':
            # if a max_depth selected by user
            if request.json['max_depth'] != '':
                sc.df_crawl(sc.domain, 0, int(request.json['max_depth']))
            else:
                sc.df_crawl(sc.domain)
        else:
            sc.bf_crawl()

        return jsonify(sc.site_map)

    template = jinja_env.get_template('index.html')
    form = DomainForm()

    return render_template(template, form=form, styles_url=url_for('static', filename='main.css'), js_url=url_for('static', filename='main.js'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8080'))
    application.run(host='0.0.0.0', port=port)
