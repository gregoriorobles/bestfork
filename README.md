# bestfork
SATToSE Hackaton project

Given a GitHub project URL, it retrieves information about its forks
and currently calculates the <a href="http://www.pylint.org">PyLint</a> rating
for each of the forks.

The result is a list of the forks of the repository sorted by this rating.

The app is composed of a server side (that uses Django) and a client side (see
the gh-pages branch).

Requirements:
  * Python
  * Django
  * PyLint
