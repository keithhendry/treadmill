"""Context plugin."""


def api_scope():
    """Returns admin API DNS scope.
    return [<my region> + '.' + 'region', '<default>.region']
    """
    assert False


def dns_domain():
    """Returns TREADMILL dns domain.

    return 'treadmill.xx.com'
    """
    assert False


def ldap_suffix():
    """Returns ldap search base.

    return 'dc=xx,dc=com'
    """
    assert False


def scopes():
    """Returns supported scopes for given cell.

    return ['campus', 'region']
    """
    assert False
