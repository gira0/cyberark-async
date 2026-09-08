User Management
======================

Manage Vault users and groups asynchronously through the ``EPV.user`` and
``EPV.group`` interfaces. The API reference below is grouped by the resource
you want to manage.

Users
---------------------------
.. currentmodule:: aiobastion.users.User
.. autofunction:: get_logged_on_user_details
.. autofunction:: list
.. autofunction:: get_id
.. autofunction:: exists
.. autofunction:: details
.. autofunction:: groups
.. autofunction:: safes
.. autofunction:: add_ssh_key
.. autofunction:: get_ssh_keys
.. autofunction:: del_ssh_key
.. autofunction:: del_all_ssh_keys
.. autofunction:: add
.. autofunction:: delete

Groups
---------------------------
.. currentmodule:: aiobastion.users.Group
.. autofunction:: list
.. autofunction:: get_id
.. autofunction:: details
.. autofunction:: add
.. autofunction:: delete
.. autofunction:: members
.. autofunction:: add_member
.. autofunction:: del_member