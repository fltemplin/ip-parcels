This distribution assumes that the "ip-parcels" hierarchy appears in the
user's ~/src directory alongside the fully expanded vanilla source hierarchies
for the public domain ION-DTN/ion-open-source-4.1.0 and kernel/linux-5.10.67.
The modified files in the ip-parcels hierarchy will be used to patch certain
files in the vanilla ION and linux kernel hierarchies prior to building.

To overwrite the vanilla ION and linux kernel files with the ip-parcels
patches, the crude scripts "ION.out" and "KERNEL.out" are provided but with
no documentation nor warranty. If you choose to use these scripts, please
read them first to make sure your source hierarchies are all set up properly
BEFORE running the scripts. If your source hierarchies become corrupted,
simply re-install from the vanilla publicly released source tarfiles and
start over.
