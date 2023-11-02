import chevron

# Chevron escapes some html signs as '&'.
# We never want this to happen.
chevron.renderer._html_escape = lambda s: s
