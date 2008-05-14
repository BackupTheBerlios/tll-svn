==========================
"tll" version 0.2.1 README
==========================
:Author: Miki Tebeka <miki.tebeka@gmail.com>
:Date: $Date$

.. contents::

What is "tll"
=============
tll is a very minimal application launcher for Linux based systems.

If you are on Mac try QuickSilver_, on Windows try Launchy_ or SlickRun_.

Installation
============
Just place `tll` somewhere in your path and edit `~/.tllrc`.

Running
=======
Assign a keystroke to invoke it [#]_ and you're done.

`tll` has a simple history, hit <UP-ARROW> or <DOWN-ARROW> to scroll the
history.

Configuration File
==================
`$HOME/.tllrc` has the following syntax:
::
    
    # tll Aliases

    www = firefox
    mail = thunderbird
    term = Terminal
    oo = soffice
    im = pidgin

Downloading etc
===============
See http://developer.berlios.de/projects/tll/.


.. _QuickSilver: http://quicksilver.blacktree.com/
.. _SlickRun: http://www.bayden.com/SlickRun/
.. _Launchy: http://www.launchy.net/
.. [#] I map <CTRL-SHIFT-K> using "Settings->Keyboard Settings->Shortcuts" in
       XFCE_.
.. _XFCE: http://www.xfce.org


.. comment: vim:ft=rst spell
