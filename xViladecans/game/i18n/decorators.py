from functools import wraps
from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.core.urlresolvers import resolve
from django.http.response import Http404
from django.shortcuts import redirect
from django.utils import translation


def load_text(fn):
    """Load language text collection from mongodb and put it in the context"""
    @wraps(fn)
    def _decorator(*args, **kwargs):

        request = None
        for arg in args:
            if isinstance(arg, WSGIRequest):
                request = arg
                break

        # Language not set by process_lang go out.
        if 'lang' not in request.session:
            return fn(*args, **kwargs)

        #@cache_partial(key="text_%s" % request.lang)
        #def _load_text():
        #    return

        #print "Loading text for lang " + request.session['lang']
        #request.session['text'] = {doc["page"]: JSONEncoder().encode(doc) for doc in settings.MONGODB.text.find({"lang": request.session['lang']})}
        request.session['text'] = {doc["page"]: doc for doc in settings.MONGODB.text.find({"lang": request.session['lang']})}

        for doc in request.session['text'].keys():
            del request.session['text'][doc]['_id']

        return fn(*args, **kwargs)
    return _decorator


def process_lang(fn):
    """Get the language from url or add it"""
    @wraps(fn)
    def _decorator(request, *args, **kwargs):
        request = None
        for arg in args:
            if isinstance(arg, WSGIRequest):
                request = arg
            if isinstance(arg, dict):
                dic_args = arg

        #print "Detecting lang"

        #enabled only for methods to display pages
        if request.method not in ["GET", "HEAD", "POST"]:
            return fn(*args, **kwargs)

        # If the url musn't receive the lang parameter continue (language-independent functions).
        if not dic_args.has_key("lang"):
            return fn(*args, **kwargs)

        # Get the url path
        url_path = request.path
        # Get the navigator language if it isn't in the database it's set to defined default language
        default_lang = 'ca'
        if default_lang not in settings.LANGUAGES_MONGO: default_lang = settings.DEFAULT_LANGUAGE


        # Get url lang
        lang = dic_args.get("lang")

        if lang is None or lang not in settings.LANGUAGES_MONGO:

            try:
                if 'lang' not in request.session.keys() or request.session['lang'] is None:
                    url = "/" + default_lang + url_path.replace("/%s" % lang, "")
                else:
                    url = "/" + request.session['lang'] + url_path.replace("/%s" % lang, "")

                match = resolve(url)
            except Http404:
                print "Could not find prepended view => 404"
                raise Http404
            except:
                print "Other error"
                raise
            else:
                return redirect(url, *match.args, **match.kwargs)

        request.session['lang'] = lang

        return fn(*args, **kwargs)
    return _decorator