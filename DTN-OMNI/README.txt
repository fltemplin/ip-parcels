This is a very terse "howto" for setting up the DTN-OMNI test environment
and running tests. (This is for testing on dedicated hardware platforms;
see DTN-CORE for running in CORE environments.) Send questions to:

1) Environment
The goal is to test LTP/UDP performance between fast processors interconnected
by a fast link (1Gbps or greater Ethernet). If you have two baremetal machines,
install Ubuntu 20.04 and run an Ethernet cable between them. The Ethernet ports
must be dedicated for testing, so use the wifi or a different Ethernet port for
general-purpose networking. If you only have an engineering laptop or other
machine capable of running Vmware or VirtualBox, set up a Ubuntu 20.04 VM and
install CORE. Once you have an environment set up, place this tarfile in your
Ubuntu home directory on each test machine and untar it there to create a
directory named "DTN-OMNI". The tarfile contains CORE *imn files that used to
work with old testing environments. They most likely will not work in this
environment, but could provide a starting point to create working CORE models.

Before running any tests, add the following lines to the end of the file
/etc/sysctl.conf. You will have to reboot for these commands to take efffect.

# Local settings for AERO/OMNI/DTN
net.core.rmem_max=134217728
net.core.wmem_max=134217728
net.core.rmem_default=134217728
net.core.wmem_default=134217728

2) Software Download
Next, download the following public domain software distributions:

ION-DTN:
********
- go to https://sourceforge.net/projects/ion-dtn/files
- download the file ion-open-source-4.1.0.tar.gz
- make a directory ~/src/ION-DTN under your Ubuntu home directory
- cd into ~/src/ION-DTN and untar the ion tarball there

linux kernel:
*************
- go to http://www.kernel.org/pub/linux/kernel/v5.x
- download the file linux-5.10.67.tar.xz
- make a directory ~/src/kernel under your Ubuntu home directory
- cd into ~/src/kernel and untar the kernel tarball there

3) Software build
The 'ip-parcels' distribution includes patched source file hierarchies under
./ip-parcels/kernel and ./ip-parcels/ION-DTN. Instructions included in the
'ip-parcels' top-level directory explain how to patch the corresponding
vanilla source distributions with the ip-parcels patches. Once the patches
have been installed, proceed as follows:

ION-DTN build:
**************
- go to ~/src/ION-DTN/ion-open-source-4.1.0
- build and install using the following commands (should take 5-10mins):

# ./configure --enable-bpv6 CFLAGS="-DUDP_MULTISEND -DMULTISEND_SEGMENT_SIZE=64000 -DMULTISEND_BATCH_LIMIT=2 -DLTPGSO -DLTPGRO -DLTPPARCEL -DLTPGSO_LIMIT=8 -DLTPSTAT -DLTPRATE"

# make
# sudo make install
# sudo ldconfig

NOTE: - See: ~/src/ip-parcels/ION-DTN/README.ion-dtn for other configure
commands to try, as many IP parcels options are enabled/disabled based on
configure-time options. After changing a configuration, you may need to run
"make clean" before again running "make" in order for the configuration
changes to take effect.

linux kernel build:
*******************
- go to ~/src/kernel/linux-5.10.67
- type: "make menuconfig"
- "down-arrow" to scroll down to "Networking support" then hit "enter"
- "down-arrow" to scroll down to "Networking options" then "enter"
- "down-arrow" to "IP: tunneling" then hit space bar till it shows "*"
- "down-arrow" to "The IPv6 protocol", "space" to show "*", then "enter"
- "down-arrow" to "IPv6: IP-in-IPv6 tunnel (RFC2473)" then "space" to show "*"
- keep hitting "< Exit >" at the bottom of the screen until it says: "Do you
  wish to save your new configuration?" - select "< Yes >".

Next, build and install the kernel with the following commands (this may
take as long as 15-30minutes or even longer; as long as it looks like it
is still making progress, let it continue):

# make -j4
# sudo make modules_install
# sudo make install

Note that linux kernel builds can proceed in unpredictable ways under
the myriad various architectures they may be run under. Specific kernel
build instructions are out of scope for this document and must be worked
out according to the specific situation.

4) Running tests
Next, reboot into the new linux kernel you just installed. You may need
to consult documentation on how to select the correct kernel at boot time.
This is necessary to access the IP parcels support code in the kernel.

We note at least one instance where booting the ip-parcels custom kernel
causes the boot to hang indefinitely. If this happens under ubuntu, try
the following steps:

a) boot into stock kernel
b) sudo vi /etc/initramfs-tools/initramfs.conf
   /* search for MODULES and edit it such that it looks like below */
c) MODULES=DEP
d) sudo update-initramfs -c -k 5.10.67
e) reboot to get into 5.10.67


Once you have booted into the new kernel decide which of the two machines
will be the "source" and which will be the "sink".

First, on both the "source" and "sink", edit the three files named
"ion_nodes" located under the DTN-OMNI/configs hierarchy and change
"fltemplin" to your Ubuntu username. Also, very importantly, edit the
"~/.bashrc" file in your home directory on both "source" and "sink" and
add the following line as the last line in the file:

export ION_NODE_LIST_DIR=.

Next, on the "source", cd into ~/DTN-OMNI/configs/20-ipn-ltp then edit the
file called "OMNI" and change "dev eno1" to "dev xyz", where "xyz" is the
name of whatever Ethernet device you have dedicated as the test port. Then,
set up the tunnel interface and verify that it got created properly by typing:

# sudo ./OMNI
# ifconfig omni0

If you see configuration lines for "omni0" with inet address 192.168.0.1,
it is set up correctly. Otherwise, go back and retrace previous instructions
to see what is missing. Send email if you can't figure it out.

On the "sink", cd into ~/DTN-OMNI/configs/25-ipn-ltp. Then, edit the "OMNI"
file and run the OMNI commands the same as you did on the "source". This time,
the "omni0" interface should show address 192.168.0.2.

On both the "source" and "sink", now run the commands:

# source ~/.bashrc
# ./ionstart

This should run through a progression showing various ION daemons getting
started. Once the ION environment is up (i.e., once ionstart completes) it
is now time to run the first test. On the "sink", type the command:

# bpcounter ipn:25.1 100

once it starts printing: "Bundles received: 0" then go back to the "source"
and type the command:

# bpdriver 100 ipn:20.1 ipn:25.1 -1000000

The "sink" should now start showing non-zero "Bundles received". If it does
not, something is wrong and you need to go retrace the steps above.

After running the test, most likely the "sink" will not have counted all
the way to "100" and exited - it will most likely be stuck on an almost
done number like: "98" and remain there indefinitely. This is due to
UDP packet loss. To get a sense for what happened, you can turn on
ltp debugging by rerunning configure with the "-DLTPDEBUG=1" option. Then
rerun the tests and look at the file "ion.log" on both the "source" and
"sink". Especially on the "sink" there will be huge volumes of diagnostics
printed out because LTPDEBUG is enabled.

The first test is set up to run with a 1280 byte segment size. To try
different segment sizes (e.g., 1400, 4000, 8000, etc.) edit the file
"node.ltprc" and uncomment the line you want to test while commmenting
out all others. Next, REBOOT BOTH MACHINES. It is the only way to clear
out the running ION daemons and flush all of the cached state. When
the machines come back up, repeat the same startup steps as above
but first either remove "ion.log" or save it off to an alternate
filename; otherwise, "ion.log" will grow indefinitely with each test.

Note: you will NOT have to run the "source ~/.bashrc" command again
after the first time, as it will be run for you at login time.

5) Experiementing with configuration settings
In ION, several configuration settings determine how GSO/GRO and
sendmmsg()/recvmmsg() will work. These are selected at configure
time. To experiment with different settings:

- go to ~/src/ION-DTN/ion-open-source-4.1.0
- run the command "make clean"
- run "configure" again with various settings per
  ~/src/ip-parcels/ION-DTN/README.ion-dtn.

(To turn on ltp debugging, add "-DLTPDEBUG=1" to the configuration. When
LTPDEBUG is enabled, the ion.log files will include huge numbers of lines
of diagnostics after each run.)

Appendix A: Compile-time options for ION-DTN performance code
The following compile-time options are now available to enable the GSO/GRO
code changes. The compile time options are included in the CFLAGS=""
directive when running "./configure".

The following options can only be used when UDP_MULTISEND is also enabled:

  -DLTPGSO - enables GSO
  -DLTPGRO - enables GRO
  -DLTPGSO_LIMIT=N - limits GSO to N segments per message (N between 1 and 64)

The following options enable code that can be used either with or without
GSO/GRO and MULTISEND:

  -DLTPRATE - enables rate limiting
  -DLTPSTAT - enabless counting number of send/receive segments

Appendix B: Rate Limiting
On some hardware platforms, unconstrained senders can cause significant
packet loss resulting in failure to deliver all bundles. When this happens,
the sender needs to institute rate limiting. To institute rate limiting,
run configure with "-DLTPRATE" in the CFLAGS, then type:

# touch ltp/udp/*.[csh]
# make
# sudo make install
# sudo ldconfig

NOTE: this step is now required to turn on rate limiting even when the
UDP_MULTISEND, LTPGSO and LTPGRO functions are disabled.
