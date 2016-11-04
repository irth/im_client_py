==============
IM Client [1]_
==============

.. image:: https://travis-ci.org/irth/im_client_py.svg?branch=master
    :target: https://travis-ci.org/irth/im_client_py

What is it?
-----------
It is (or rather: will be) a **highly modular universal instant messaging client**.
Plugins will run as separate processes communicating over a TCP/Unix socket (encryption will be available).
The server will allow plugins to communicate easily. Plugins will provide UIs and connections to chat networks.

Why?
----
I was inspired to make this software while using a combination of two products.
It may or may not have been a messaging app made by a big social network with a blue logo,
running on a smartphone that may or may not have been made by a South Korean phonemaker.

Basically it exasperates me that because of a bloated stock ROM my phone has only 300MB of RAM available out of 1GB that is installed even when no apps are running, and that the messaging app takes the remaining 300MB.

Also I'd love to have the chat head feature on IRC. (pls dont sue).

I plan on making an Android app that can connect to the server as a plugin and allow me to chat easily on any chat service without talking all of my resources.

How to install it?
------------------
Well I guess you can just
::
    python setup.py install
or something but there's not much to install yet.

Tests can be run just by calling "tox" in the command line, assuming you've got it installed.

.. [1] It's not the final name