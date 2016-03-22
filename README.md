# ParliamentTree

An application which aims to help the public to engage with the happenings of the UK parliament.

It is current in its infacy and we are looking for developers and interface designers to help us.


## Functionality Aims

Allow user to see what their MP (and other MPs) have said in parliament and to:

* Like or dislike individual speeches.
* Vote on speeches which contain statistics to be fact checked (the most voted speeches may be submitted to [fullfact.org](https://fullfact.org/) for checking).
* Flag speeches as being [filibustering](https://en.wikipedia.org/wiki/Filibuster).
* View the most opinion-generating speeches each week.  (Opinion measured by `sum(likes, dislikes)`.)
* Receive notifications when:
  - Their MP says something which generates a lot of opinion.
  - Their MP says something which gets fact checked.
  - A keyword which they have specified is mentioned by an MP.
* Users could potentially subscribe to MPs other than their own, although the idea is to give a broader view of parliament, rather than just headlines about famous MPs.


## Implementation

### Web Application

This will use data from [Hansard](http://www.parliament.uk/business/publications/hansard/) and save it into a database, and will provide the processing systems and API for the mobile apps to use.
The web application can also have a user-face UI if we want.

The plan is to build the web application in Python using Django and hosting it on Google App Engine
This means that there will be some unfamiliar aspects to the DB side of things for developers who aren't used to using Django on a non-relational database,
but it means that we'll be on a DB which can scale to huge amounts of data (and traffic, if necesary) as the app grows over time.

### iOS Application

This will use the API provided by the web app (and possibly using some web views provided by the web app).
We'll probably use [Cordova](https://cordova.apache.org/docs/en/2.5.0/guide/getting-started/ios/).

### Android Application

Pretty much ditto to iOS.


### Blackberry Application

Lolz



## Get Involved!

See the CONTRIBUTING.md file for info on getting involved.
