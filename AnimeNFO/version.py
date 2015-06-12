__version__ = '0.3'
HOME_PAGE = 'http://github.com/kfdm/radio-growl'


def default_user_agent(name='radio-growl'):
	return 'radio-growl {0} {1}'.format(__version__, HOME_PAGE)
