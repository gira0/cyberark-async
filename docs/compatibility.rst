Component compatibility
===============================

PVWA
-------
Versions known to be compatible today are 12.2.x and 12.6.x and 14.x.

If you have an older version, some functions won't work and you'll raise a CyberarkException "Your PVWA version does not support this function".

This version was initially developed for version 12.1, then updated for version 12.2.
We've made every effort to keep the package backward-compatible with version 12.1, but for technical reasons we can only test on one version at a time and can't guarantee this 100%.
If you find any inconsistencies, please don't hesitate to create an issue.

All new versions of this package will be tested on version 12.6.x.

AIM
------
All versions of AIM that we were able to test (v12+) were compatible with this package.

aiobastion
----------
This package is a fork of `aiobastion <https://github.com/safepost/aiobastion>`_.
It is installed with ``pip install cyberark-async`` and imported as ``cyberark_async``.

The import name was changed from ``aiobastion`` so that both packages can be installed side by side without overwriting each other.
There is no ``aiobastion`` compatibility module. To migrate code written for aiobastion:

* Replace ``import aiobastion`` with ``import cyberark_async``, and ``from aiobastion...`` with ``from cyberark_async...``.
* ``AiobastionException`` and ``AiobastionConfigurationException`` are now ``CyberarkAsyncException`` and ``CyberarkAsyncConfigurationException``. The old names still work as aliases.
* The library logs to the ``cyberark_async`` logger instead of ``aiobastion``.
