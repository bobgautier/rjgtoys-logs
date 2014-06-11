
:class:`LogPoint`: A better way to create logs
==============================================

This module provides an alternative to the traditional text-based logging interface.

What's wrong with logging?
--------------------------

A log file is traditionally a human-readable, if sometimes terse and cryptic, 'stream of consciousness' commentary on the operation
of a program, that can be used for a number of purposes:

* to provide feedback to the user
* to provide information for problem diagnosis
* to assist with debugging
* to support various kinds of audit
* to drive monitoring and alerting
* metric collection

Whilst it would be a stretch to say that logs are not designed at all, many logs
show signs of having more to do with the implementation of a piece of software than its design:

* Inconsistent message format
* Inconsistent level of granularity
* Debug logging in particular is often (naturally) based on development-time debugging - "if in doubt, print"
* Frequency and verbosity: messages are written too frequently, or too much information is included with every message.
* Inappropriate content: stack traces presented to users for example
* Security risks: usernames, passwords, commercially sensitive data included in logs
 
There can also be 'errors of omission', when information is omitted because the programmer decided it
would make the log too big, or if the information is hard to format into a simple piece of text.

Log scraping
------------

Logs are often used to provide information for monitoring; so-called "log scraping" checks logs for messages
that indicate situations that need attention.

The parsers used by monitoring probes are often very primitive, little more than a 'grep' for lines of interest (which is
fine because a few false positives are not going to be much of a problem).

However the principle of extracting information from logs is now being supported directly by packages such
as logstash, which incorporates a relatively sophisticated pattern matching engine to convert (textual) log
entries into sets of key-value pairs.  Those key-value pairs are captured in a database which supports searching, sorting, indexing and so on.

This parsing of log messages is often described as (re)capture of semantic information from the logs.

Systems such as logstash centralise the parsing of log messages, make the grammar definition more explicit and
provide more powerful parsers than are usually included in monitoring scripts.  Those scripts are simplified
because the parsing of messages is delegated to something else, and they can concentrate on identifying alert conditions.


But whereever it is done, parsing of log messages creates a dependency on an interface (the log format) that is not explicitly provided
by the producer of the log.   Under no commitment to a particular log entry format, an implementor may change it or remove it altogether when the package is updated.

Even if the code that produces the messages is stable, parsing them may be inherently unreliable, for example if user-provided text is included in the message (so that, for example, quotes or parentheses might not be matched).


If the information contained in textual logs is of use to other programs, why not emit it in a more usable form in the first place?
There are better ways to provide it than going via text.

Message routing and filtering
-----------------------------

Existing logging interfaces such as :mod:`logging` provide a way to insert messages into a log stream, and
can be configured to split the stream of messages to multiple destinations, depending on, for example, the module that
logged the message and a severity indicator (e.g. ``DEBUG`` or ``INFO``).

Routing can also be used to filter messages (route to '/dev/null')

Routing based on origin allows logs for a subcomponent to be separated from those for higher level components.

Routing based on severity is often used to allow the amount of detail collected to be controlled ('turn on debug logging')

It would be possible to route messages based on their content too, by parsing the messages.

Problems:

* the question of *role* is ignored: a *user* of a program and its *administrator* might need different information, the *supporter* or *developer* different information again.   What constitutes 'debug' information for a *user* is likely to be different to that expected by a *developer*
* filtering and routing are usually configured in advance, but the need for a higher level of detail can't always be forseen, and sometimes it's impossible to retry an operation simply to create more detailed logs

How :mod:`logpoint` does it better
----------------------------------

* It makes preserving the semantics of log entries easier; log entries are sets of key-value pairs, not text strings
* It allows log entries to be associated with *roles* so that they can be routed appropriately
* Routing of messages may be based on any attribute(s) of a log entry, without the need to parse any text
* Filtering of messages prior to their storage is discouraged.  Filtering is best done by tools that query the log, not by programs that create them.
* Creation of a log entry is not just a line of code; a :class:`LogPoint` is an entity in a module in its own right that should be documented as a part of a module interface in the same way that its classes and exceptions are.

The user interface of a program may include a component that listens for log entries directed at the "user" role, filters them according to user preferences, and presents the remainder to the user.

