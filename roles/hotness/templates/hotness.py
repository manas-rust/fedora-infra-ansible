import os
import socket
hostname = socket.gethostname().split('.', 1)[0]

description_template = """Latest upstream release: %(latest_upstream)s

Current version/release in %(repo_name)s: %(repo_version)s-%(repo_release)s

URL: %(url)s


Please consult the package updates policy before you
issue an update to a stable branch:
https://fedoraproject.org/wiki/Updates_Policy


More information about the service that created this bug can be found at:

%(explanation_url)s
"""

config = {
    'hotness.bugzilla.enabled': True,

    'hotness.bugzilla': {
        'user': '{{ bugzilla_user }}',
        'password': '{{ bugzilla_password }}',
{% if env == 'staging' %}
        'url': 'https://partner-bugzilla.redhat.com',
        'explanation_url': 'https://stg.fedoraproject.org/wiki/Upstream_release_monitoring',
{% else %}
        'url': 'https://bugzilla.redhat.com',
        'explanation_url': 'https://fedoraproject.org/wiki/Upstream_release_monitoring',
{% endif %}
        'product': 'Fedora',
        'version': 'rawhide',
        'keywords': 'FutureFeature,Triaged',
        'bug_status': 'NEW',
        'short_desc_template': "%(name)s-%(latest_upstream)s is available",
        'description_template': description_template,
    },

    'hotness.koji': {
{% if env == 'staging' %}
        'server': 'https://koji.stg.fedoraproject.org/kojihub',
        'weburl': 'http://koji.stg.fedoraproject.org/koji',
        # TODO - I'd like to use staging gitolite, but it is broken right now?
        #'git_url': 'http://pkgs.stg.fedoraproject.org/cgit/{package}.git',
        'git_url': 'http://pkgs01.phx2.fedoraproject.org/cgit/{package}.git',
{% else %}
        'server': 'https://koji.fedoraproject.org/kojihub',
        'weburl': 'http://koji.fedoraproject.org/koji',
        'git_url': 'http://pkgs01.phx2.fedoraproject.org/cgit/{package}.git',
{% endif %}

        # This cert is generated by sshing as root to fas01 and running
        #     $ cd /var/lib/fedora-ca
        #     $ python certhelper.py normal --outdir=/var/tmp/ \
        #               --name=hotness --cadir=. --caname=Fedora
        # Then scp the cert to lockbox01 into the private dir.
        'cert': '/etc/pki/fedmsg/hotness.pem',
        'ca_cert': '/etc/pki/fedmsg/fedora-server-ca.cert',

        'userstring': ('Fedora Release Monitoring '
                       '<release-monitoring@fedoraproject.org>'),
        'opts': {'scratch': True},
        'priority': 30,
        'target_tag': 'rawhide',
    },

{% if env == 'staging' %}
    'hotness.pkgdb_url': 'https://admin.stg.fedoraproject.org/pkgdb/api',
{% else %}
    'hotness.pkgdb_url': 'https://admin.fedoraproject.org/pkgdb/api',
{% endif %}

    'hotness.yumconfig': '/etc/hotness-yum.conf',

    "hotness.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 300,
        "arguments": {
            "filename": "/var/tmp/the-new-hotness-cache.dbm",
        },
    },
}

