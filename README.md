# NP

## Setup the SFTP user

`sudo apt-get install openssh-server`

`sudo groupadd sftpusers`

`sudo useradd -g sftpusers -d /var/www/photo-networks-hosting/ -s /sbin/nologin pn-sftp-user`

Change the password:
`passwd pn-sftp-user`

Test if everything is fine
cat /etc/passwd | grep pn-sftp-user

Nope Add permisions chown -R sftpuser:sftpusers /data/dirstatinfo/csvfiles

Configure ssh protocole
$ vim /etc/ssh/sshd_config

Subsystem sftp internal-sftp
Match Group sftpusers
ChrootDirectory /path/to/files
ForceCommand internal-sftp

Enable Chroot
setsebool -P ssh_chroot_rw_homedirs=1

Restart the ssh service
/etc/init.d/sshd restart

Be careful, the Chroot is on the main folder and the chown to the local user in the subfolders
