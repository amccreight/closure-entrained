closure-entrained
=================

Analysis of analysis for variables unnecessarily entrained by inner functions.

Right now this lets you specify a whitelist, and then filter out the
entrained vars that are on the whitelist.

To generate the analysis of variables unnecessarily entrained by inner
functions, use a debug build of the spidermonkey shell with the option
--dump-entrained-variables.  See bug 894669 for more details.