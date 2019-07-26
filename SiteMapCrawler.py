from flask import Flask, render_template, request, url_for, jsonify
from forms import DomainForm
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
    Simple index file renderer
    :return: Rendered index.html
    '''
    template = jinja_env.get_template('index.html')
    form = DomainForm()

    return render_template(template, form=form, styles_url=url_for('static', filename='main.css'), js_url=url_for('static', filename='main.js'), map_url=url_for('make_map'))


@application.route('/make-map', methods=['POST'])
def make_map():
    '''
    Handles site crawl/map generation
    :param domain: String value representing the domain to crawl/generate a map for
    :return: JSONResponse
        if domain is valid, JSON document representing the domain's site map in the structure:
            [
                {
                    "page_url": <a_url>,
                    "links": <all_links_on_page>,
                    "images:" <all_img_links_on_page>
                },
                ...
            ]
        if domain invalid: {"info": "Invalid domain"}
    '''
    domain = request.get_data('domain')

    return jsonify('hi')


if __name__=='__main__':
    port = int(os.environ.get('PORT', '8080'))
    application.run(host='0.0.0.0', port=port)