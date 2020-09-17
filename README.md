# Intertextual Canon Cloud 2

## About

Intertextual Canon Cloud is a platform for displaying and annotating texts in a
collaborative way. A wiki for annotations, if you will. It is a spiritual
successor to the long defunct [Textus Project](http://okfnlabs.org/textus/).
Note: this project has nothing to do with that project except similar aims and
that I will be hewing to their design decisions in this new iteration.

The primary deployment of this software, in fact the *only* deployment of this
software, can be viewed at [anno.wiki](https://anno.wiki)

Intertextual Canon Cloud 2 is a ground up rewrite of the initial software that
can be found [here](https://github.com/malan88/icc).

## Prospectus

Screw it. We're doing a ground up rewrite.

anno.wiki has never caught on. I have learned a lot since I initially designed
it, but more importantly, I have learned a lot of hard design lessons. The
initial version of icc, which took about a year to write, was a failure.

I am therefore undergoing a complete redesign of the software from the ground
up, and will be hewing more closely to the separation of concerns strategy used
by Textus.

Ethan will be collaborating with me, hopefully, when he has time. I will also
continue the job search. I am hoping that with my much-improved understanding of
Flask, general web design, and the actual requirements of the project from
already having built the thing once, the development will go more quickly.

Ethan will be "in charge" of the front end, though I expect I will be writing
the majority of the code (he has a full time job). I will defer to him on design
decisions. I will be in charge of everything else.

This project will use React on the front end and Flask on the back end. We will
be separating all formatting and semantic information from the raw text of the
text-to-be-annotated. It will be immutable.

The database is still to be determined. I am still learning toward
elasticsearch, since that is what Textus used and I am somewhat familiar with
it. I have gotten some recommendations for databases specifically designed for
our use case on [Reddit](https://www.reddit.com/r/Database/comments/iuktng/database_recommendation_question/)
and am interested in exploring them.

We will have to use another database for User information. I am leaning toward
Postgres.

Stay tuned for future updates, my nonexistent readers.
