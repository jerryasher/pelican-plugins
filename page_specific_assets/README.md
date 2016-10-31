Page Specific Assets
===============

This Pelican plugin makes it easy to embed Javascript files and CSS stylesheets into individual Pelican blog articles.

Credit
------
This plugin was inspired by and adopted from the work of [ ]() at

which was based on Rob Story's [Pelican Dynamic](https://github.com/wrobstory) at [pelican_dynamic](https://github.com/wrobstory/pelican_dynamic). 


Installation
------------
To install the plugin, [follow the instructions on the Pelican plugin page.](https://github.com/getpelican/pelican-plugins) My settings look like the following:

```python
PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['pelican_javascript']
```

Directory Structure
-------------------
Create ```js``` and ```css``` directories in your ```content``` directory:
```
website/
├── content
│   ├── js/
│   │   └── page1.js
│   │   └── page2.js
│   ├── css/
│   │   └── page1.css
│   ├── article1.rst
│   ├── cat/
│   │   └── article2.md
│   └── pages
│       └── about.md
└── pelicanconf.py
```

and then specify each resource as a comma-separated file name in the ```scripts``` and ```stylesheets``` keys

```
Title: Pelican blog post with dynamic javascript and css components
Date: 2016-10-08
Category: blog
Tags: trig and shapes
Author: Jerry Asher
scripts: page1.js, page2.js
stylesheets: page1.css
```

You can also include javascript libraries from a web resource without having to carry the files on your own. Using the ```libs``` key, If the string starts with `http://` or `https://` it will be treated like a web resource

```
Title: Pelican blog post with dynamic javascript and css components
Date: 2016-10-08
Category: blog
Tags: trig and shapes
Author: Jerry Asher
script: page1.js, page2.js
stylesheet: page1.css
libs: https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js,
```

You can reference and load google fonts using the ```google-fonts``` key and providing a google font selector (see [Google Fonts](https://fonts.google.com/))

```
Title: Pelican blog post with dynamic javascript and css components
Date: 2016-10-08
Category: blog
Tags: trig and shapes
Author: Jerry Asher
script: page1.js, page2.js
stylesheet: page1.css
libs: https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js,
google-font: Oswald:400,700
```


You can add style fragments directly into the header with the ```style``` key:

```
Title: Pelican blog post with dynamic javascript and css components
Date: 2016-10-08
Category: blog
Tags: trig and shapes
Author: Jerry Asher
script: page1.js, page2.js
stylesheet: page1.css
libs: https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js,
google-font: Oswald:400,700
style: body { font-family: 'Oswald', sans-serif; font-size: 100%; }
```

And you can define short tags for well known libraries in the config file that are then referenced with the libs key.

```
EXTERNAL_PAGE_LIBS = {
    'jquery': 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js',
    'threejs': 'https://ajax.googleapis.com/ajax/libs/threejs/r76/three.min.js'
}
```

and then


Title: Pelican blog post with dynamic javascript and css components
Date: 2016-10-08
Category: blog
Tags: trig and shapes
Author: Jerry Asher
scripts: page1.js, page2.js
stylesheets: page1.css
libs: jquery, threejs
google-font: Oswald:400,700
style: body { font-family: 'Oswald', sans-serif; font-size: 100%; }


Note that the files will be included in the same order specified.

Additions to Templates
----------------------
Finally, in your base template (likely named ```base.html```), you need to add the following in your ```<head>``` section of the HTML:
```
{% if article %}
    {% if article.stylesheets %}
        {% for stylesheet in article.stylesheets %}
{{ stylesheet }}
        {% endfor %}
    {% endif %}
    {% if article.styles %} 
       {% for style in article.stylesheets %}
{{ style }}
        {% endfor %}
    {% endif %}
{% endif %}
```
and the following *after* your ```</body>``` tag:
```
{% if article %}
    {% if article.javascripts %}
        {% for javascript in article.javascripts %}
{{ javascript }}
        {% endfor %}
    {% endif %}
{% endif %}
```

That's it! Run your standard ```make html``` or ```make publish``` commands and your JSS/CSS will be moved and referenced in the output HTML.
