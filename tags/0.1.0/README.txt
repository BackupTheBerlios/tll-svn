===============================
"launchie" version 0.1.0 README
===============================
:Author: Miki Tebeka <miki.tebeka@gmail.com>
:Data: $Date$

.. contents::


What is "lanuchie"
==================
Launchie is a very minimal application launcher for Linux based systems.

If you are on Mac try QuickSilver_, on Windows try SlickRun_.

Installation
============
Just place `launchie` somewhere in your path and edit `~/.lauchierc`.

Running
=======
Assign a keystroke to invoke it [#]_ and you're done.

Configuration File
==================
`$HOME/.lauchierc` has the following syntax:
::
    
    # Launchie Aliases

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
.. [#] I map <CTRL-SHIFT-K> using "Settings->Keyboard Settings->Shortcuts" in
       XFCE_.
.. _XFCE: http://www.xfce.org


.. comment: vim:ft=rst spell
