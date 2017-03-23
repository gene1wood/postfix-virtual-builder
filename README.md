Tool to modify a [postfix virtual file mapping](http://www.postfix.org/VIRTUAL_README.html)
to configure an entire domain for which all email sent to any user @ that domain
will be delivered to a single email address with the exception of a specific
set of usernames.

# Usage

1. Modify the `build_postfix_virtual.yaml` configuration
2. Run `python build_postfix_virtual.py` to render the values in the `yaml`
   configuration into the `/etc/postfix/virtual` configuration file

# Example

Here is an example config

    ---
    addresses:
      - name: john.example.com
        blocked_domains:
          - southernrailway.com
          - offthegridsf.com
          - fusionbeads.com
          - cb.com
        recipient: john.doe@example.edu
      - name: jane.example.com
        blocked_domains:
          - boxee.tv
          - tools.ltb-project.org
          - budsgunshop.com
        recipient: jane.doe@example.org

In this example `john.example.com` is a domain that John uses to create unique
email addresses for each web site he creates an account at. For example John
uses the email address `facebook.com@john.example.com` when he signs up for a
facebook account and `twitter.com@john.example.com` when he signs up for a
twitter account. 

`john.doe@example.edu` is John's actual email address that he
wants all of his facebook and twitter notifications delivered to.

The `blocked_domains` list is a list of sites where john has created an account
and the site subsequently sold his email address to marketers, was hacked or
published his email address publicly on the internet. As a result spam email
is now routinely sent to those email addresses and John wants to block them.

In this example John signed up for an account at `southernrailway.com` using the
email address `southernrailway.com@john.example.com`. `southernrailway.com`
subsequently sold his email address to marketers and spam is now being sent to
that address. By including it in the `blocked_domains` list, those emails will
be rejected.

This would result in a postfix `/etc/postfix/virtual` config of

    /^(?!southernrailway\.com@|offthegridsf\.com@|fusionbeads\.com@|cb\.com@).*@john\.example\.com$/  john.doe@example.edu
    /^(?!boxee\.tv@|tools\.ltb-project\.org@|budsgunshop\.com@).*@jane\.example\.com$/  jane.doe@example.org
