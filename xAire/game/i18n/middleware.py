from game.i18n.decorators import load_text, process_lang


class ContextMiddleware(object):
	@process_lang
	@load_text
	def process_view(self, request, view_func, *view_args, **view_kwargs):
		return None