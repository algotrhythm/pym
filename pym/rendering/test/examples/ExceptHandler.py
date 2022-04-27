try:
    pass
except:  # noqa
    pass

try:
    pass
except Exception:
    pass

try:
    pass
except Exception as e:
    x = e

try:
    pass
except (Exception, SyntaxError) as e:
    x = e
