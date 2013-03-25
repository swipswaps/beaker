
"""
bkr system-power: Control power for a Beaker system
===================================================

.. program:: bkr system-power

Synopsis
--------

| :program:`bkr system-power` [*options*]
|       [--action=<action>] [--clear-netboot] [--force] <fqdn>

Description
-----------

Controls power for a Beaker system using its remote power management interface 
(if one is available).

Options
-------

.. option:: --action <action>

   Perform the given power action. Valid actions are ``on``, ``off``, 
   and ``reboot``. The default is ``reboot``.

.. option:: --clear-netboot

   Clear any existing netboot configuration before performing this action. This 
   will ensure the system falls back to booting from its local hard disk.

.. option:: --force

   Normally this command will refuse to run if another user is using the 
   system. Pass this option to perform the power action anyway.

Common :program:`bkr` options are described in the :ref:`Options 
<common-options>` section of :manpage:`bkr(1)`.

Exit status
-----------

Non-zero on error, otherwise zero.

Examples
--------

Power off a particular system::

    bkr system-power --action off system2.example.invalid

See also
--------

:manpage:`bkr-system-provision(1)`, :manpage:`bkr(1)`
"""

from bkr.client import BeakerCommand

class System_Power(BeakerCommand):
    """Control power for a system"""
    enabled = True

    valid_actions = ('on', 'off', 'interrupt', 'reboot')

    def options(self):
        self.parser.usage = "%%prog %s [options] <fqdn>" % self.normalized_name
        self.parser.add_option('--action', metavar='ACTION',
                help='Perform ACTION (on, off, interrupt, or reboot) [default: %default]')
        self.parser.add_option('--clear-netboot', action='store_true',
                help="Clear system's netboot configuration "
                     "before performing action")
        self.parser.add_option('--force', action='store_true',
                help='Perform action even if system is '
                     'currently in use by another user')
        self.parser.set_defaults(action='reboot', force=False)

    def run(self, *args, **kwargs):
        if len(args) != 1:
            self.parser.error('Exactly one system fqdn must be given')
        fqdn = args[0]

        if kwargs['action'] not in self.valid_actions:
            self.parser.error('Power action must be one of: %r'
                    % (self.valid_actions,))

        self.set_hub(**kwargs)
        self.hub.systems.power(kwargs['action'], fqdn,
                kwargs['clear_netboot'], kwargs['force'])
