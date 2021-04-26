## Install Guide ##
In order to install this plugin you will need to first set up a broker box with Python installed on it. Once this is done carry out the following steps;
1. Ensure that python and pip are installed on the system you wish to run as the brokwe box.
1. Install the pip requirements from the requirments file <code>python3 -m pip install -r requirments.txt</code>
1. Set up the configurations settings in teh config.json file.
1. Ensure to also set up the configuration for the SMTP.SSL code point in the read_mailbox.py script.
1. chmod +x the py files so they can run.
1. Test out the read_mailbox.py to ensure you can read the email within the mailbox (This will only read unread emails and mark them as read once finished.)

### Automation ###
If You wish to set this script up to automatically run on a scheduled basis then you can either put it in a systemd process or create a cron job for it.
