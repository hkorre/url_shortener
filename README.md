# url_shortener
URL Shortener


## How to run

There is a docker container that contains all the dependencies.
* $ cd docker
* $ ./build.sh
* $ ./run.sh

If need to attach a second terminal:
$ ./attach.sh

You can then wget a zip of the repo into the docker.

Note: If you don't use the docker, the system probably won't work because
the server uses 0.0.0.0:8888 as the address, which is not the default of localhost:5000
that is normally run outside docker.


To run the system:
* $ cd src
* $ build_database.py
* $ python server.py

You can access the swagger UI outside the docker by going to:
localhost:8888/api/ui/

The commands all work through the UI except for the redirect.
For redirects, just put in:
http://localhost:8888/api/{slug}

You could modify this in server.py if you'd like to change the address.


## Decisions

### slug type

Slugs are 7 characters long and consist of lower case letters, upper case letters, and numbers 0-9.
The types of characters are to make the url easy for the user to type. The length is based on being
as short as possible while also providing an adequate number of addresses to last the lifetime of
the service.

### endpoints

The enpoints are pretty simple.
/{slug} makes the url really short for redirection
/shortlinks and /shortlinks/{slug} follow the convention of the path aligning to resources.

/cleanup is also an endpoint. That way we can run a cron job, say weekly, that would easily call the
endpoint with a curl command.

### parameters

Path - slugs are in the path because they are under the shortlinks resource.
Query - modifying the expiration date is part of the query because they are optional.
Body - destination is part of the body because it's required but not a resource

