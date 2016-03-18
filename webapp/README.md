# Parliament Tree Web Application

## Functionality

* Get data of what's said in parliament from Hansard, store it in the DB.  Updated daily (hourly?) using a cron job.
* Store user accounts (of the public), including:
  - The MP of each user (based on their location/post code)
  - Any other MPs that they want to follow
  - Any keywords that they want to follow
* When new speeches are saved, work out which users need to be notified based on who/what they're following.
* Provide (an) API(s) for the mobile apps to get feeds/notifications/etc.
* Possibly provide a web-based interface for users (we might make the phone apps by embedding web views).


## Architecture

Built in Python using [Django](https://djangoproject.com) and [Djangae](https://github.com/potatolondon/djangae).
Hosted on Google App Engine.

The use of Google App Engine and its non-relational, schemaless DB means that some aspects will be unfamiliar to "normal" Django developers.
See [Djangae documentation](https://djangae.readthedocs.org) and [App Engine documentation](https://cloud.google.com/appengine/docs/python/).


## Contributing

Note that the code is under the MIT license, and that by contributing you are releasing those contributions under the same license.

See the GitHub issues for things to work on.
