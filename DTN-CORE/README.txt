This is a runtime enviroment suitale for starting the ION-DTN services in
a CORE model. First, locate and install the CORE network emulation package
from https://github.com/coreemu/core. Next, find and edit three files named
"ion_nodes" and replace the string "/home/fltemplin" with "/home/<username>"
which is your username and also the top-level directory where DTN-CORE must
reside.

Next, edit your home ~/.bashrc file and add the following line to the end:

export ION_NODE_LIST_DIR=.

Next, start core with:

  # sudo core-daemon start
  # core-gui

Then, in the CORE gui, open the file DTN-CORE.1.0.1.imn and start the
model. When the model comes up, open terminal windows on nodes 20 and
25 then in each window type the following:

Node 25:
# su <username>
# cd ~/DTN-CORE/25-ipn-ltp
# bpcounter ipn:25.1 100

Node 20:
# su <username>
# cd ~/DTN-CORE/20-ipn-ltp
# bpdriver 100 ipn:20.1 ipn:25.1 -1000000

This will run a performance test, which may or may not succeed. To run
successive tests, rerun the bpcounter/bpdriver commands - always starting
bpcounter first before running bpdriver. If no progress is made, try
restarting the CORE model and start from scratch. If still no progress,
try setting he bpdriver/bpcounter repetition counter to something smaller
than 100 (e.g., 10, 1, etc.) and try again after a clean restart.

As experience is gained with running the tests, make adjustments to the
node.ltprc files as necessary to run additional tests while stopping and
restarting the CORE model and repeating the above commands for each test.

IMPORTANT NOTE: Newer versions of the CORE network emulator are switching
over to use *.xml configuration files instead of the legacy *.imn. The new
CORE gui will therefore fail to open the *imn files included in this distro.
If this is a problem, first try looking for "core-gui-legacy" under the
same install directory where "core-gui" was installed and try to open the
*imn files with the legacy gui. If the legacy gui is not found or will not
open the *.imn, consider reverting to an older version of CORE - CORE
version 7.5.2 is known to work well.
