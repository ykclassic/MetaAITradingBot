Run docker build -t nexus-smc-engine:latest .
#0 building with "default" instance using docker driver

#*** [internal] load build definition from Dockerfile
#*** transferring dockerfile: ***.32kB done
#*** WARN: FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 2)
#*** DONE 0.0s

#2 [auth] library/python:pull token for registry-***.docker.io
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.9-slim
#3 DONE 0.4s

#4 [internal] load .dockerignore
#4 transferring context: 2B done
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 42***.***0kB 0.0s done
#5 DONE 0.0s

#6 [builder ***/5] FROM docker.io/library/python:3.9-slim@sha256:2d97f69***0b***6bd338d3060f26***f53f***44965f755599aab***acda***e***3cf***73***b***b
#6 resolve docker.io/library/python:3.9-slim@sha256:2d97f69***0b***6bd338d3060f26***f53f***44965f755599aab***acda***e***3cf***73***b***b done
#6 sha256:b3ec39b36ae8c03a3e09854de4ec4aa0838***dfed84a9daa075048c2e3df388***d ***.29MB / ***.29MB 0.***s done
#6 sha256:fc74430849022d***3b0d44b8969a953f842f59c6e9d***a0c2c83d7***0affa286c08 0B / ***3.88MB 0.***s
#6 sha256:ea56f685404adf8***680322f***52d2cfec62***5b30dda48***c2c4500783***5beb508 0B / 25***B 0.***s
#6 sha256:2d97f69***0b***6bd338d3060f26***f53f***44965f755599aab***acda***e***3cf***73***b***b ***0.36kB / ***0.36kB done
#6 sha256:dad5b29e3506c35e0fd222736f4d4ef25d2***b2***9acdd73f7bb4***d59996ca8e0d ***.74kB / ***.74kB done
#6 sha256:085da638e***b8a4495***4c3fda83ff50a3bffae44***8b050cfacd87e572207***f497 5.40kB / 5.40kB done
#6 sha256:385***3bd72563***3495cdd83b3b09***5a633cfa475dc2a07072ab2c8d***9***020ca5d ***9.92MB / 29.78MB 0.***s
#6 sha256:fc74430849022d***3b0d44b8969a953f842f59c6e9d***a0c2c83d7***0affa286c08 ***3.88MB / ***3.88MB 0.***s done
#6 sha256:ea56f685404adf8***680322f***52d2cfec62***5b30dda48***c2c4500783***5beb508 25***B / 25***B 0.***s done
#6 sha256:385***3bd72563***3495cdd83b3b09***5a633cfa475dc2a07072ab2c8d***9***020ca5d 29.78MB / 29.78MB 0.***s done
#6 extracting sha256:385***3bd72563***3495cdd83b3b09***5a633cfa475dc2a07072ab2c8d***9***020ca5d 0.***s
#6 extracting sha256:385***3bd72563***3495cdd83b3b09***5a633cfa475dc2a07072ab2c8d***9***020ca5d 0.9s done
#6 extracting sha256:b3ec39b36ae8c03a3e09854de4ec4aa0838***dfed84a9daa075048c2e3df388***d 0.***s done
#6 extracting sha256:fc74430849022d***3b0d44b8969a953f842f59c6e9d***a0c2c83d7***0affa286c08
#6 extracting sha256:fc74430849022d***3b0d44b8969a953f842f59c6e9d***a0c2c83d7***0affa286c08 0.6s done
#6 extracting sha256:ea56f685404adf8***680322f***52d2cfec62***5b30dda48***c2c4500783***5beb508
#6 extracting sha256:ea56f685404adf8***680322f***52d2cfec62***5b30dda48***c2c4500783***5beb508 done
#6 DONE 5.0s

#7 [builder 2/5] WORKDIR /app
#7 DONE 0.0s

#8 [stage-*** 3/6] RUN groupadd -r nexus && useradd -r -g nexus nexus
#8 DONE 0.2s

#9 [builder 3/5] RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     gcc     && rm -rf /var/lib/apt/lists/*
#9 0.2***4 Get:*** http://deb.debian.org/debian trixie InRelease [***40 kB]
#9 0.227 Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
#9 0.228 Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
#9 0.255 Get:4 http://deb.debian.org/debian trixie/main amd64 Packages [9673 kB]
#9 0.3***4 Get:5 http://deb.debian.org/debian trixie-updates/main amd64 Packages [44***2 B]
#9 0.3***5 Get:6 http://deb.debian.org/debian-security trixie-security/main amd64 Packages [236 kB]
#9 ***.0***3 Fetched ***0.*** MB in ***s (***2.5 MB/s)
#9 ***.0***3 Reading package lists...
#9 ***.506 Reading package lists...
#9 ***.997 Building dependency tree...
#9 2.***6 Reading state information...
#9 2.27*** The following additional packages will be installed:
#9 2.27***   binutils binutils-common binutils-x86-64-linux-gnu bzip2 cpp cpp-***4
#9 2.27***   cpp-***4-x86-64-linux-gnu cpp-x86-64-linux-gnu dpkg dpkg-dev g++ g++-***4
#9 2.27***   g++-***4-x86-64-linux-gnu g++-x86-64-linux-gnu gcc-***4 gcc-***4-x86-64-linux-gnu
#9 2.272   gcc-x86-64-linux-gnu libasan8 libatomic*** libbinutils libc-bin libc-dev-bin
#9 2.272   libc6 libc6-dev libcc***-0 libcrypt-dev libctf-nobfd0 libctf0 libdpkg-perl
#9 2.272   libgcc-***4-dev libgdbm-compat4t64 libgomp*** libgprofng0 libhwasan0 libisl23
#9 2.272   libitm*** libjansson4 liblsan0 liblzma5 libmpc3 libmpfr6 libperl5.40
#9 2.272   libquadmath0 libsframe*** libstdc++-***4-dev libtsan2 libubsan*** linux-libc-dev
#9 2.273   make patch perl perl-modules-5.40 rpcsvc-proto xz-utils
#9 2.273 Suggested packages:
#9 2.273   binutils-doc gprofng-gui binutils-gold bzip2-doc cpp-doc gcc-***4-locales
#9 2.273   cpp-***4-doc debian-keyring debian-tag2upload-keyring g++-multilib
#9 2.273   g++-***4-multilib gcc-***4-doc gcc-multilib manpages-dev autoconf automake
#9 2.273   libtool flex bison gdb gcc-doc gcc-***4-multilib gdb-x86-64-linux-gnu
#9 2.273   libc-devtools glibc-doc sq | sqop | rsop | gosop | pgpainless-cli | gpg-sq
#9 2.273   | gnupg sensible-utils git bzr libstdc++-***4-doc make-doc ed diffutils-doc
#9 2.273   perl-doc libterm-readline-gnu-perl | libterm-readline-perl-perl
#9 2.273   libtap-harness-archive-perl
#9 2.273 Recommended packages:
#9 2.273   fakeroot sq | sqop | rsop | gosop | pgpainless-cli | gpg-sq | gnupg
#9 2.273   libalgorithm-merge-perl manpages manpages-dev libfile-fcntllock-perl
#9 2.273   liblocale-gettext-perl
#9 2.473 The following NEW packages will be installed:
#9 2.473   binutils binutils-common binutils-x86-64-linux-gnu build-essential bzip2 cpp
#9 2.473   cpp-***4 cpp-***4-x86-64-linux-gnu cpp-x86-64-linux-gnu dpkg-dev g++ g++-***4
#9 2.473   g++-***4-x86-64-linux-gnu g++-x86-64-linux-gnu gcc gcc-***4
#9 2.473   gcc-***4-x86-64-linux-gnu gcc-x86-64-linux-gnu libasan8 libatomic*** libbinutils
#9 2.473   libc-dev-bin libc6-dev libcc***-0 libcrypt-dev libctf-nobfd0 libctf0
#9 2.473   libdpkg-perl libgcc-***4-dev libgdbm-compat4t64 libgomp*** libgprofng0
#9 2.473   libhwasan0 libisl23 libitm*** libjansson4 liblsan0 libmpc3 libmpfr6
#9 2.474   libperl5.40 libquadmath0 libsframe*** libstdc++-***4-dev libtsan2 libubsan***
#9 2.474   linux-libc-dev make patch perl perl-modules-5.40 rpcsvc-proto xz-utils
#9 2.475 The following packages will be upgraded:
#9 2.475   dpkg libc-bin libc6 liblzma5
#9 2.503 4 upgraded, 52 newly installed, 0 to remove and ***2 not upgraded.
#9 2.503 Need to get 87.9 MB of archives.
#9 2.503 After this operation, 336 MB of additional disk space will be used.
#9 2.503 Get:*** http://deb.debian.org/debian trixie/main amd64 dpkg amd64 ***.22.22 [***537 kB]
#9 2.5***6 Get:2 http://deb.debian.org/debian trixie/main amd64 libc6 amd64 2.4***-***2+deb***3u3 [2850 kB]
#9 2.527 Get:3 http://deb.debian.org/debian trixie/main amd64 libc-bin amd64 2.4***-***2+deb***3u3 [638 kB]
#9 2.53*** Get:4 http://deb.debian.org/debian trixie/main amd64 liblzma5 amd64 5.8.***-***+deb***3u*** [309 kB]
#9 2.532 Get:5 http://deb.debian.org/debian trixie/main amd64 bzip2 amd64 ***.0.8-6 [40.5 kB]
#9 2.533 Get:6 http://deb.debian.org/debian trixie/main amd64 perl-modules-5.40 all 5.40.***-6 [30***9 kB]
#9 2.544 Get:7 http://deb.debian.org/debian trixie/main amd64 libgdbm-compat4t64 amd64 ***.24-2 [50.3 kB]
#9 2.544 Get:8 http://deb.debian.org/debian trixie/main amd64 libperl5.40 amd64 5.40.***-6 [434*** kB]
#9 2.560 Get:9 http://deb.debian.org/debian trixie/main amd64 perl amd64 5.40.***-6 [267 kB]
#9 2.56*** Get:***0 http://deb.debian.org/debian trixie/main amd64 xz-utils amd64 5.8.***-***+deb***3u*** [659 kB]
#9 2.564 Get:*** http://deb.debian.org/debian trixie/main amd64 libsframe*** amd64 2.44-3 [78.4 kB]
#9 2.564 Get:***2 http://deb.debian.org/debian trixie/main amd64 binutils-common amd64 2.44-3 [2509 kB]
#9 2.575 Get:***3 http://deb.debian.org/debian trixie/main amd64 libbinutils amd64 2.44-3 [534 kB]
#9 2.577 Get:***4 http://deb.debian.org/debian trixie/main amd64 libgprofng0 amd64 2.44-3 [808 kB]
#9 2.580 Get:***5 http://deb.debian.org/debian trixie/main amd64 libctf-nobfd0 amd64 2.44-3 [***56 kB]
#9 2.58*** Get:***6 http://deb.debian.org/debian trixie/main amd64 libctf0 amd64 2.44-3 [88.6 kB]
#9 2.582 Get:***7 http://deb.debian.org/debian trixie/main amd64 libjansson4 amd64 2.***4-2+b3 [39.8 kB]
#9 2.583 Get:***8 http://deb.debian.org/debian trixie/main amd64 binutils-x86-64-linux-gnu amd64 2.44-3 [***0***4 kB]
#9 2.586 Get:***9 http://deb.debian.org/debian trixie/main amd64 binutils amd64 2.44-3 [265 kB]
#9 2.587 Get:20 http://deb.debian.org/debian trixie/main amd64 libc-dev-bin amd64 2.4***-***2+deb***3u3 [59.8 kB]
#9 2.589 Get:2*** http://deb.debian.org/debian-security trixie-security/main amd64 linux-libc-dev all 6.***2.***0***-*** [290*** kB]
#9 2.595 Get:22 http://deb.debian.org/debian trixie/main amd64 libcrypt-dev amd64 ***:4.4.38-*** [***9 kB]
#9 2.596 Get:23 http://deb.debian.org/debian trixie/main amd64 rpcsvc-proto amd64 ***.4.3-*** [63.3 kB]
#9 2.596 Get:24 http://deb.debian.org/debian trixie/main amd64 libc6-dev amd64 2.4***-***2+deb***3u3 [***992 kB]
#9 2.603 Get:25 http://deb.debian.org/debian trixie/main amd64 libisl23 amd64 0.27-*** [659 kB]
#9 2.606 Get:26 http://deb.debian.org/debian trixie/main amd64 libmpfr6 amd64 4.2.2-*** [729 kB]
#9 2.609 Get:27 http://deb.debian.org/debian trixie/main amd64 libmpc3 amd64 ***.3.***-***+b3 [52.2 kB]
#9 2.6***0 Get:28 http://deb.debian.org/debian trixie/main amd64 cpp-***4-x86-64-linux-gnu amd64 ***4.2.0-***9 [***.0 MB]
#9 2.648 Get:29 http://deb.debian.org/debian trixie/main amd64 cpp-***4 amd64 ***4.2.0-***9 [***280 B]
#9 2.648 Get:30 http://deb.debian.org/debian trixie/main amd64 cpp-x86-64-linux-gnu amd64 4:***4.2.0-*** [4840 B]
#9 2.648 Get:3*** http://deb.debian.org/debian trixie/main amd64 cpp amd64 4:***4.2.0-*** [***568 B]
#9 2.649 Get:32 http://deb.debian.org/debian trixie/main amd64 libcc***-0 amd64 ***4.2.0-***9 [42.8 kB]
#9 2.650 Get:33 http://deb.debian.org/debian trixie/main amd64 libgomp*** amd64 ***4.2.0-***9 [***37 kB]
#9 2.650 Get:34 http://deb.debian.org/debian trixie/main amd64 libitm*** amd64 ***4.2.0-***9 [26.0 kB]
#9 2.650 Get:35 http://deb.debian.org/debian trixie/main amd64 libatomic*** amd64 ***4.2.0-***9 [9308 B]
#9 2.65*** Get:36 http://deb.debian.org/debian trixie/main amd64 libasan8 amd64 ***4.2.0-***9 [2725 kB]
#9 2.660 Get:37 http://deb.debian.org/debian trixie/main amd64 liblsan0 amd64 ***4.2.0-***9 [***204 kB]
#9 2.665 Get:38 http://deb.debian.org/debian trixie/main amd64 libtsan2 amd64 ***4.2.0-***9 [2460 kB]
#9 2.674 Get:39 http://deb.debian.org/debian trixie/main amd64 libubsan*** amd64 ***4.2.0-***9 [***074 kB]
#9 2.678 Get:40 http://deb.debian.org/debian trixie/main amd64 libhwasan0 amd64 ***4.2.0-***9 [***488 kB]
#9 2.684 Get:4*** http://deb.debian.org/debian trixie/main amd64 libquadmath0 amd64 ***4.2.0-***9 [***45 kB]
#9 2.684 Get:42 http://deb.debian.org/debian trixie/main amd64 libgcc-***4-dev amd64 ***4.2.0-***9 [2672 kB]
#9 2.694 Get:43 http://deb.debian.org/debian trixie/main amd64 gcc-***4-x86-64-linux-gnu amd64 ***4.2.0-***9 [2***.4 MB]
#9 2.767 Get:44 http://deb.debian.org/debian trixie/main amd64 gcc-***4 amd64 ***4.2.0-***9 [540 kB]
#9 2.769 Get:45 http://deb.debian.org/debian trixie/main amd64 gcc-x86-64-linux-gnu amd64 4:***4.2.0-*** [***436 B]
#9 2.770 Get:46 http://deb.debian.org/debian trixie/main amd64 gcc amd64 4:***4.2.0-*** [5***36 B]
#9 2.770 Get:47 http://deb.debian.org/debian trixie/main amd64 libstdc++-***4-dev amd64 ***4.2.0-***9 [2376 kB]
#9 2.778 Get:48 http://deb.debian.org/debian trixie/main amd64 g++-***4-x86-64-linux-gnu amd64 ***4.2.0-***9 [***2.*** MB]
#9 2.820 Get:49 http://deb.debian.org/debian trixie/main amd64 g++-***4 amd64 ***4.2.0-***9 [22.5 kB]
#9 2.820 Get:50 http://deb.debian.org/debian trixie/main amd64 g++-x86-64-linux-gnu amd64 4:***4.2.0-*** [***200 B]
#9 2.820 Get:5*** http://deb.debian.org/debian trixie/main amd64 g++ amd64 4:***4.2.0-*** [***344 B]
#9 2.820 Get:52 http://deb.debian.org/debian trixie/main amd64 make amd64 4.4.***-2 [463 kB]
#9 2.822 Get:53 http://deb.debian.org/debian trixie/main amd64 libdpkg-perl all ***.22.22 [65*** kB]
#9 2.825 Get:54 http://deb.debian.org/debian trixie/main amd64 patch amd64 2.8-2 [***34 kB]
#9 2.826 Get:55 http://deb.debian.org/debian trixie/main amd64 dpkg-dev all ***.22.22 [***337 kB]
#9 2.83*** Get:56 http://deb.debian.org/debian trixie/main amd64 build-essential amd64 ***2.***2 [4624 B]
#9 2.945 debconf: unable to initialize frontend: Dialog
#9 2.945 debconf: (TERM is not set, so the dialog frontend is not usable.)
#9 2.945 debconf: falling back to frontend: Readline
#9 2.946 debconf: unable to initialize frontend: Readline
#9 2.946 debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC entries checked: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.40.*** /usr/local/share/perl/5.40.*** /usr/lib/x86_64-linux-gnu/perl5/5.40 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.40 /usr/share/perl/5.40 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 8, <STDIN> line 56.)
#9 2.946 debconf: falling back to frontend: Teletype
#9 2.950 debconf: unable to initialize frontend: Teletype
#9 2.950 debconf: (This frontend requires a controlling tty.)
#9 2.950 debconf: falling back to frontend: Noninteractive
#9 3.920 Preconfiguring packages ...
#9 3.963 Fetched 87.9 MB in 0s (254 MB/s)
#9 3.976 (Reading database ... 
(Reading database ... 5%
(Reading database ... ***0%
(Reading database ... ***5%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... ***00%
(Reading database ... 5644 files and directories currently installed.)
#9 3.983 Preparing to unpack .../dpkg_***.22.22_amd64.deb ...
#9 3.985 Unpacking dpkg (***.22.22) over (***.22.2***) ...
#9 4.063 Setting up dpkg (***.22.22) ...
#9 4.***82 (Reading database ... 
(Reading database ... 5%
(Reading database ... ***0%
(Reading database ... ***5%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... ***00%
(Reading database ... 5644 files and directories currently installed.)
#9 4.***87 Preparing to unpack .../libc6_2.4***-***2+deb***3u3_amd64.deb ...
#9 4.254 debconf: unable to initialize frontend: Dialog
#9 4.254 debconf: (TERM is not set, so the dialog frontend is not usable.)
#9 4.254 debconf: falling back to frontend: Readline
#9 4.254 debconf: unable to initialize frontend: Readline
#9 4.254 debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC entries checked: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.40.*** /usr/local/share/perl/5.40.*** /usr/lib/x86_64-linux-gnu/perl5/5.40 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.40 /usr/share/perl/5.40 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 8.)
#9 4.254 debconf: falling back to frontend: Teletype
#9 4.26*** debconf: unable to initialize frontend: Teletype
#9 4.26*** debconf: (This frontend requires a controlling tty.)
#9 4.26*** debconf: falling back to frontend: Noninteractive
#9 4.309 Unpacking libc6:amd64 (2.4***-***2+deb***3u3) over (2.4***-***2) ...
#9 4.535 Setting up libc6:amd64 (2.4***-***2+deb***3u3) ...
#9 4.596 debconf: unable to initialize frontend: Dialog
#9 4.596 debconf: (TERM is not set, so the dialog frontend is not usable.)
#9 4.596 debconf: falling back to frontend: Readline
#9 4.596 debconf: unable to initialize frontend: Readline
#9 4.596 debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC entries checked: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.40.*** /usr/local/share/perl/5.40.*** /usr/lib/x86_64-linux-gnu/perl5/5.40 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.40 /usr/share/perl/5.40 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 8.)
#9 4.596 debconf: falling back to frontend: Teletype
#9 4.60*** debconf: unable to initialize frontend: Teletype
#9 4.60*** debconf: (This frontend requires a controlling tty.)
#9 4.60*** debconf: falling back to frontend: Noninteractive
#9 4.636 (Reading database ... 
(Reading database ... 5%
(Reading database ... ***0%
(Reading database ... ***5%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... ***00%
(Reading database ... 5644 files and directories currently installed.)
#9 4.642 Preparing to unpack .../libc-bin_2.4***-***2+deb***3u3_amd64.deb ...
#9 4.643 Unpacking libc-bin (2.4***-***2+deb***3u3) over (2.4***-***2) ...
#9 4.69*** Setting up libc-bin (2.4***-***2+deb***3u3) ...
#9 4.7***7 (Reading database ... 
(Reading database ... 5%
(Reading database ... ***0%
(Reading database ... ***5%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... ***00%
(Reading database ... 5644 files and directories currently installed.)
#9 4.72*** Preparing to unpack .../liblzma5_5.8.***-***+deb***3u***_amd64.deb ...
#9 4.724 Unpacking liblzma5:amd64 (5.8.***-***+deb***3u***) over (5.8.***-***) ...
#9 4.746 Setting up liblzma5:amd64 (5.8.***-***+deb***3u***) ...
#9 4.762 Selecting previously unselected package bzip2.
#9 4.762 (Reading database ... 
(Reading database ... 5%
(Reading database ... ***0%
(Reading database ... ***5%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... ***00%
(Reading database ... 5644 files and directories currently installed.)
#9 4.767 Preparing to unpack .../00-bzip2_***.0.8-6_amd64.deb ...
#9 4.768 Unpacking bzip2 (***.0.8-6) ...
#9 4.783 Selecting previously unselected package perl-modules-5.40.
#9 4.784 Preparing to unpack .../0***-perl-modules-5.40_5.40.***-6_all.deb ...
#9 4.784 Unpacking perl-modules-5.40 (5.40.***-6) ...
#9 5.029 Selecting previously unselected package libgdbm-compat4t64:amd64.
#9 5.030 Preparing to unpack .../02-libgdbm-compat4t64_***.24-2_amd64.deb ...
#9 5.03*** Unpacking libgdbm-compat4t64:amd64 (***.24-2) ...
#9 5.046 Selecting previously unselected package libperl5.40:amd64.
#9 5.047 Preparing to unpack .../03-libperl5.40_5.40.***-6_amd64.deb ...
#9 5.048 Unpacking libperl5.40:amd64 (5.40.***-6) ...
#9 5.265 Selecting previously unselected package perl.
#9 5.266 Preparing to unpack .../04-perl_5.40.***-6_amd64.deb ...
#9 5.267 Unpacking perl (5.40.***-6) ...
#9 5.290 Selecting previously unselected package xz-utils.
#9 5.29*** Preparing to unpack .../05-xz-utils_5.8.***-***+deb***3u***_amd64.deb ...
#9 5.292 Unpacking xz-utils (5.8.***-***+deb***3u***) ...
#9 5.324 Selecting previously unselected package libsframe***:amd64.
#9 5.325 Preparing to unpack .../06-libsframe***_2.44-3_amd64.deb ...
#9 5.326 Unpacking libsframe***:amd64 (2.44-3) ...
#9 5.34*** Selecting previously unselected package binutils-common:amd64.
#9 5.342 Preparing to unpack .../07-binutils-common_2.44-3_amd64.deb ...
#9 5.342 Unpacking binutils-common:amd64 (2.44-3) ...
#9 5.457 Selecting previously unselected package libbinutils:amd64.
#9 5.459 Preparing to unpack .../08-libbinutils_2.44-3_amd64.deb ...
#9 5.460 Unpacking libbinutils:amd64 (2.44-3) ...
#9 5.498 Selecting previously unselected package libgprofng0:amd64.
#9 5.499 Preparing to unpack .../09-libgprofng0_2.44-3_amd64.deb ...
#9 5.500 Unpacking libgprofng0:amd64 (2.44-3) ...
#9 5.549 Selecting previously unselected package libctf-nobfd0:amd64.
#9 5.550 Preparing to unpack .../***0-libctf-nobfd0_2.44-3_amd64.deb ...
#9 5.55*** Unpacking libctf-nobfd0:amd64 (2.44-3) ...
#9 5.570 Selecting previously unselected package libctf0:amd64.
#9 5.57*** Preparing to unpack .../***-libctf0_2.44-3_amd64.deb ...
#9 5.57*** Unpacking libctf0:amd64 (2.44-3) ...
#9 5.588 Selecting previously unselected package libjansson4:amd64.
#9 5.589 Preparing to unpack .../***2-libjansson4_2.***4-2+b3_amd64.deb ...
#9 5.589 Unpacking libjansson4:amd64 (2.***4-2+b3) ...
#9 5.603 Selecting previously unselected package binutils-x86-64-linux-gnu.
#9 5.604 Preparing to unpack .../***3-binutils-x86-64-linux-gnu_2.44-3_amd64.deb ...
#9 5.605 Unpacking binutils-x86-64-linux-gnu (2.44-3) ...
#9 5.684 Selecting previously unselected package binutils.
#9 5.686 Preparing to unpack .../***4-binutils_2.44-3_amd64.deb ...
#9 5.688 Unpacking binutils (2.44-3) ...
#9 5.7***2 Selecting previously unselected package libc-dev-bin.
#9 5.7***4 Preparing to unpack .../***5-libc-dev-bin_2.4***-***2+deb***3u3_amd64.deb ...
#9 5.7***4 Unpacking libc-dev-bin (2.4***-***2+deb***3u3) ...
#9 5.729 Selecting previously unselected package linux-libc-dev.
#9 5.730 Preparing to unpack .../***6-linux-libc-dev_6.***2.***0***-***_all.deb ...
#9 5.73*** Unpacking linux-libc-dev (6.***2.***0***-***) ...
#9 6.040 Selecting previously unselected package libcrypt-dev:amd64.
#9 6.042 Preparing to unpack .../***7-libcrypt-dev_***%3a4.4.38-***_amd64.deb ...
#9 6.047 Unpacking libcrypt-dev:amd64 (***:4.4.38-***) ...
#9 6.064 Selecting previously unselected package rpcsvc-proto.
#9 6.065 Preparing to unpack .../***8-rpcsvc-proto_***.4.3-***_amd64.deb ...
#9 6.066 Unpacking rpcsvc-proto (***.4.3-***) ...
#9 6.083 Selecting previously unselected package libc6-dev:amd64.
#9 6.084 Preparing to unpack .../***9-libc6-dev_2.4***-***2+deb***3u3_amd64.deb ...
#9 6.085 Unpacking libc6-dev:amd64 (2.4***-***2+deb***3u3) ...
#9 6.20*** Selecting previously unselected package libisl23:amd64.
#9 6.203 Preparing to unpack .../20-libisl23_0.27-***_amd64.deb ...
#9 6.204 Unpacking libisl23:amd64 (0.27-***) ...
#9 6.246 Selecting previously unselected package libmpfr6:amd64.
#9 6.248 Preparing to unpack .../2***-libmpfr6_4.2.2-***_amd64.deb ...
#9 6.249 Unpacking libmpfr6:amd64 (4.2.2-***) ...
#9 6.278 Selecting previously unselected package libmpc3:amd64.
#9 6.279 Preparing to unpack .../22-libmpc3_***.3.***-***+b3_amd64.deb ...
#9 6.280 Unpacking libmpc3:amd64 (***.3.***-***+b3) ...
#9 6.295 Selecting previously unselected package cpp-***4-x86-64-linux-gnu.
#9 6.296 Preparing to unpack .../23-cpp-***4-x86-64-linux-gnu_***4.2.0-***9_amd64.deb ...
#9 6.297 Unpacking cpp-***4-x86-64-linux-gnu (***4.2.0-***9) ...
#9 6.687 Selecting previously unselected package cpp-***4.
#9 6.689 Preparing to unpack .../24-cpp-***4_***4.2.0-***9_amd64.deb ...
#9 6.689 Unpacking cpp-***4 (***4.2.0-***9) ...
#9 6.70*** Selecting previously unselected package cpp-x86-64-linux-gnu.
#9 6.703 Preparing to unpack .../25-cpp-x86-64-linux-gnu_4%3a***4.2.0-***_amd64.deb ...
#9 6.703 Unpacking cpp-x86-64-linux-gnu (4:***4.2.0-***) ...
#9 6.7***7 Selecting previously unselected package cpp.
#9 6.7***8 Preparing to unpack .../26-cpp_4%3a***4.2.0-***_amd64.deb ...
#9 6.723 Unpacking cpp (4:***4.2.0-***) ...
#9 6.736 Selecting previously unselected package libcc***-0:amd64.
#9 6.738 Preparing to unpack .../27-libcc***-0_***4.2.0-***9_amd64.deb ...
#9 6.738 Unpacking libcc***-0:amd64 (***4.2.0-***9) ...
#9 6.753 Selecting previously unselected package libgomp***:amd64.
#9 6.754 Preparing to unpack .../28-libgomp***_***4.2.0-***9_amd64.deb ...
#9 6.755 Unpacking libgomp***:amd64 (***4.2.0-***9) ...
#9 6.774 Selecting previously unselected package libitm***:amd64.
#9 6.775 Preparing to unpack .../29-libitm***_***4.2.0-***9_amd64.deb ...
#9 6.776 Unpacking libitm***:amd64 (***4.2.0-***9) ...
#9 6.790 Selecting previously unselected package libatomic***:amd64.
#9 6.792 Preparing to unpack .../30-libatomic***_***4.2.0-***9_amd64.deb ...
#9 6.793 Unpacking libatomic***:amd64 (***4.2.0-***9) ...
#9 6.807 Selecting previously unselected package libasan8:amd64.
#9 6.808 Preparing to unpack .../3***-libasan8_***4.2.0-***9_amd64.deb ...
#9 6.809 Unpacking libasan8:amd64 (***4.2.0-***9) ...
#9 6.942 Selecting previously unselected package liblsan0:amd64.
#9 6.944 Preparing to unpack .../32-liblsan0_***4.2.0-***9_amd64.deb ...
#9 6.945 Unpacking liblsan0:amd64 (***4.2.0-***9) ...
#9 7.0***3 Selecting previously unselected package libtsan2:amd64.
#9 7.0***4 Preparing to unpack .../33-libtsan2_***4.2.0-***9_amd64.deb ...
#9 7.0***5 Unpacking libtsan2:amd64 (***4.2.0-***9) ...
#9 7.***38 Selecting previously unselected package libubsan***:amd64.
#9 7.***40 Preparing to unpack .../34-libubsan***_***4.2.0-***9_amd64.deb ...
#9 7.***4*** Unpacking libubsan***:amd64 (***4.2.0-***9) ...
#9 7.20*** Selecting previously unselected package libhwasan0:amd64.
#9 7.203 Preparing to unpack .../35-libhwasan0_***4.2.0-***9_amd64.deb ...
#9 7.204 Unpacking libhwasan0:amd64 (***4.2.0-***9) ...
#9 7.282 Selecting previously unselected package libquadmath0:amd64.
#9 7.284 Preparing to unpack .../36-libquadmath0_***4.2.0-***9_amd64.deb ...
#9 7.284 Unpacking libquadmath0:amd64 (***4.2.0-***9) ...
#9 7.303 Selecting previously unselected package libgcc-***4-dev:amd64.
#9 7.304 Preparing to unpack .../37-libgcc-***4-dev_***4.2.0-***9_amd64.deb ...
#9 7.305 Unpacking libgcc-***4-dev:amd64 (***4.2.0-***9) ...
#9 7.420 Selecting previously unselected package gcc-***4-x86-64-linux-gnu.
#9 7.422 Preparing to unpack .../38-gcc-***4-x86-64-linux-gnu_***4.2.0-***9_amd64.deb ...
#9 7.423 Unpacking gcc-***4-x86-64-linux-gnu (***4.2.0-***9) ...
#9 7.897 Selecting previously unselected package gcc-***4.
#9 7.899 Preparing to unpack .../39-gcc-***4_***4.2.0-***9_amd64.deb ...
#9 7.900 Unpacking gcc-***4 (***4.2.0-***9) ...
#9 7.92*** Selecting previously unselected package gcc-x86-64-linux-gnu.
#9 7.922 Preparing to unpack .../40-gcc-x86-64-linux-gnu_4%3a***4.2.0-***_amd64.deb ...
#9 7.923 Unpacking gcc-x86-64-linux-gnu (4:***4.2.0-***) ...
#9 7.937 Selecting previously unselected package gcc.
#9 7.938 Preparing to unpack .../4***-gcc_4%3a***4.2.0-***_amd64.deb ...
#9 7.938 Unpacking gcc (4:***4.2.0-***) ...
#9 7.953 Selecting previously unselected package libstdc++-***4-dev:amd64.
#9 7.954 Preparing to unpack .../42-libstdc++-***4-dev_***4.2.0-***9_amd64.deb ...
#9 7.955 Unpacking libstdc++-***4-dev:amd64 (***4.2.0-***9) ...
#9 8.***2*** Selecting previously unselected package g++-***4-x86-64-linux-gnu.
#9 8.***23 Preparing to unpack .../43-g++-***4-x86-64-linux-gnu_***4.2.0-***9_amd64.deb ...
#9 8.***23 Unpacking g++-***4-x86-64-linux-gnu (***4.2.0-***9) ...
#9 8.5***5 Selecting previously unselected package g++-***4.
#9 8.5***7 Preparing to unpack .../44-g++-***4_***4.2.0-***9_amd64.deb ...
#9 8.5***8 Unpacking g++-***4 (***4.2.0-***9) ...
#9 8.53*** Selecting previously unselected package g++-x86-64-linux-gnu.
#9 8.532 Preparing to unpack .../45-g++-x86-64-linux-gnu_4%3a***4.2.0-***_amd64.deb ...
#9 8.533 Unpacking g++-x86-64-linux-gnu (4:***4.2.0-***) ...
#9 8.546 Selecting previously unselected package g++.
#9 8.547 Preparing to unpack .../46-g++_4%3a***4.2.0-***_amd64.deb ...
#9 8.548 Unpacking g++ (4:***4.2.0-***) ...
#9 8.560 Selecting previously unselected package make.
#9 8.56*** Preparing to unpack .../47-make_4.4.***-2_amd64.deb ...
#9 8.562 Unpacking make (4.4.***-2) ...
#9 8.592 Selecting previously unselected package libdpkg-perl.
#9 8.593 Preparing to unpack .../48-libdpkg-perl_***.22.22_all.deb ...
#9 8.594 Unpacking libdpkg-perl (***.22.22) ...
#9 8.633 Selecting previously unselected package patch.
#9 8.634 Preparing to unpack .../49-patch_2.8-2_amd64.deb ...
#9 8.635 Unpacking patch (2.8-2) ...
#9 8.653 Selecting previously unselected package dpkg-dev.
#9 8.654 Preparing to unpack .../50-dpkg-dev_***.22.22_all.deb ...
#9 8.655 Unpacking dpkg-dev (***.22.22) ...
#9 8.703 Selecting previously unselected package build-essential.
#9 8.704 Preparing to unpack .../5***-build-essential_***2.***2_amd64.deb ...
#9 8.705 Unpacking build-essential (***2.***2) ...
#9 8.726 Setting up libgdbm-compat4t64:amd64 (***.24-2) ...
#9 8.728 Setting up binutils-common:amd64 (2.44-3) ...
#9 8.730 Setting up linux-libc-dev (6.***2.***0***-***) ...
#9 8.732 Setting up libctf-nobfd0:amd64 (2.44-3) ...
#9 8.734 Setting up libgomp***:amd64 (***4.2.0-***9) ...
#9 8.735 Setting up bzip2 (***.0.8-6) ...
#9 8.737 Setting up libsframe***:amd64 (2.44-3) ...
#9 8.739 Setting up libjansson4:amd64 (2.***4-2+b3) ...
#9 8.74*** Setting up rpcsvc-proto (***.4.3-***) ...
#9 8.742 Setting up make (4.4.***-2) ...
#9 8.744 Setting up libmpfr6:amd64 (4.2.2-***) ...
#9 8.746 Setting up xz-utils (5.8.***-***+deb***3u***) ...
#9 8.750 update-alternatives: using /usr/bin/xz to provide /usr/bin/lzma (lzma) in auto mode
#9 8.750 update-alternatives: warning: skip creation of /usr/share/man/man***/lzma.***.gz because associated file /usr/share/man/man***/xz.***.gz (of link group lzma) doesn't exist
#9 8.750 update-alternatives: warning: skip creation of /usr/share/man/man***/unlzma.***.gz because associated file /usr/share/man/man***/unxz.***.gz (of link group lzma) doesn't exist
#9 8.75*** update-alternatives: warning: skip creation of /usr/share/man/man***/lzcat.***.gz because associated file /usr/share/man/man***/xzcat.***.gz (of link group lzma) doesn't exist
#9 8.75*** update-alternatives: warning: skip creation of /usr/share/man/man***/lzmore.***.gz because associated file /usr/share/man/man***/xzmore.***.gz (of link group lzma) doesn't exist
#9 8.75*** update-alternatives: warning: skip creation of /usr/share/man/man***/lzless.***.gz because associated file /usr/share/man/man***/xzless.***.gz (of link group lzma) doesn't exist
#9 8.75*** update-alternatives: warning: skip creation of /usr/share/man/man***/lzdiff.***.gz because associated file /usr/share/man/man***/xzdiff.***.gz (of link group lzma) doesn't exist
#9 8.75*** update-alternatives: warning: skip creation of /usr/share/man/man***/lzcmp.***.gz because associated file /usr/share/man/man***/xzcmp.***.gz (of link group lzma) doesn't exist
#9 8.75*** update-alternatives: warning: skip creation of /usr/share/man/man***/lzgrep.***.gz because associated file /usr/share/man/man***/xzgrep.***.gz (of link group lzma) doesn't exist
#9 8.752 update-alternatives: warning: skip creation of /usr/share/man/man***/lzegrep.***.gz because associated file /usr/share/man/man***/xzegrep.***.gz (of link group lzma) doesn't exist
#9 8.752 update-alternatives: warning: skip creation of /usr/share/man/man***/lzfgrep.***.gz because associated file /usr/share/man/man***/xzfgrep.***.gz (of link group lzma) doesn't exist
#9 8.754 Setting up libquadmath0:amd64 (***4.2.0-***9) ...
#9 8.756 Setting up libmpc3:amd64 (***.3.***-***+b3) ...
#9 8.758 Setting up libatomic***:amd64 (***4.2.0-***9) ...
#9 8.760 Setting up patch (2.8-2) ...
#9 8.762 Setting up libubsan***:amd64 (***4.2.0-***9) ...
#9 8.764 Setting up perl-modules-5.40 (5.40.***-6) ...
#9 8.765 Setting up libhwasan0:amd64 (***4.2.0-***9) ...
#9 8.767 Setting up libcrypt-dev:amd64 (***:4.4.38-***) ...
#9 8.773 Setting up libasan8:amd64 (***4.2.0-***9) ...
#9 8.776 Setting up libtsan2:amd64 (***4.2.0-***9) ...
#9 8.777 Setting up libbinutils:amd64 (2.44-3) ...
#9 8.779 Setting up libisl23:amd64 (0.27-***) ...
#9 8.78*** Setting up libc-dev-bin (2.4***-***2+deb***3u3) ...
#9 8.783 Setting up libcc***-0:amd64 (***4.2.0-***9) ...
#9 8.785 Setting up liblsan0:amd64 (***4.2.0-***9) ...
#9 8.787 Setting up libitm***:amd64 (***4.2.0-***9) ...
#9 8.788 Setting up libctf0:amd64 (2.44-3) ...
#9 8.79*** Setting up libperl5.40:amd64 (5.40.***-6) ...
#9 8.792 Setting up perl (5.40.***-6) ...
#9 8.797 Setting up libgprofng0:amd64 (2.44-3) ...
#9 8.799 Setting up cpp-***4-x86-64-linux-gnu (***4.2.0-***9) ...
#9 8.80*** Setting up libdpkg-perl (***.22.22) ...
#9 8.803 Setting up cpp-***4 (***4.2.0-***9) ...
#9 8.805 Setting up libc6-dev:amd64 (2.4***-***2+deb***3u3) ...
#9 8.807 Setting up libgcc-***4-dev:amd64 (***4.2.0-***9) ...
#9 8.809 Setting up libstdc++-***4-dev:amd64 (***4.2.0-***9) ...
#9 8.8*** Setting up binutils-x86-64-linux-gnu (2.44-3) ...
#9 8.8***3 Setting up cpp-x86-64-linux-gnu (4:***4.2.0-***) ...
#9 8.8***5 Setting up binutils (2.44-3) ...
#9 8.8***7 Setting up dpkg-dev (***.22.22) ...
#9 8.820 Setting up cpp (4:***4.2.0-***) ...
#9 8.829 Setting up gcc-***4-x86-64-linux-gnu (***4.2.0-***9) ...
#9 8.83*** Setting up gcc-x86-64-linux-gnu (4:***4.2.0-***) ...
#9 8.833 Setting up gcc-***4 (***4.2.0-***9) ...
#9 8.835 Setting up g++-***4-x86-64-linux-gnu (***4.2.0-***9) ...
#9 8.837 Setting up g++-x86-64-linux-gnu (4:***4.2.0-***) ...
#9 8.839 Setting up g++-***4 (***4.2.0-***9) ...
#9 8.84*** Setting up gcc (4:***4.2.0-***) ...
#9 8.849 Setting up g++ (4:***4.2.0-***) ...
#9 8.852 update-alternatives: using /usr/bin/g++ to provide /usr/bin/c++ (c++) in auto mode
#9 8.853 Setting up build-essential (***2.***2) ...
#9 8.856 Processing triggers for libc-bin (2.4***-***2+deb***3u3) ...
#9 DONE 9.4s

#***0 [builder 4/5] COPY requirements.txt .
#***0 DONE 0.0s

#*** [builder 5/5] RUN pip install --user --no-cache-dir -r requirements.txt
#*** ***.993 Collecting ccxt==4.2.34
#*** 2.0***6   Downloading ccxt-4.2.34-py2.py3-none-any.whl (4.2 MB)
#*** 2.048      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB ***42.6 MB/s eta 0:00:00
#*** 2.379 Collecting pandas==2.2.0
#*** 2.384   Downloading pandas-2.2.0-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (***3.0 MB)
#*** 2.468      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***3.0/***3.0 MB ***5***.*** MB/s eta 0:00:00
#*** 3.079 Collecting numpy==***.26.3
#*** 3.084   Downloading numpy-***.26.3-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (***8.2 MB)
#*** 3.***77      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***8.2/***8.2 MB ***95.7 MB/s eta 0:00:00
#*** 3.292 Collecting pyyaml==6.0.***
#*** 3.297   Downloading PyYAML-6.0.***-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (738 kB)
#*** 3.30***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 738.9/738.9 kB 286.7 MB/s eta 0:00:00
#*** 3.328 Collecting python-dotenv==***.0.***
#*** 3.332   Downloading python_dotenv-***.0.***-py3-none-any.whl (***9 kB)
#*** 3.378 Collecting requests==2.3***.0
#*** 3.38***   Downloading requests-2.3***.0-py3-none-any.whl (62 kB)
#*** 3.384      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.6/62.6 kB 260.2 MB/s eta 0:00:00
#*** 3.5***6 Collecting torch==2.2.0
#*** 3.520   Downloading torch-2.2.0-cp39-cp39-manylinux***_x86_64.whl (755.5 MB)
#*** 7.297      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 755.5/755.5 MB 222.0 MB/s eta 0:00:00
#*** 8.343 Collecting torchvision==0.***7.0
#*** 8.347   Downloading torchvision-0.***7.0-cp39-cp39-manylinux***_x86_64.whl (6.9 MB)
#*** 8.4***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.9/6.9 MB ***3.8 MB/s eta 0:00:00
#*** 8.640 Collecting scikit-learn==***.4.0
#*** 8.646   Downloading scikit_learn-***.4.0-***-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (***2.*** MB)
#*** 8.729      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***2.***/***2.*** MB ***49.4 MB/s eta 0:00:00
#*** 8.840 Collecting transformers==4.37.2
#*** 8.846   Downloading transformers-4.37.2-py3-none-any.whl (8.4 MB)
#*** 8.880      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.4/8.4 MB 262.*** MB/s eta 0:00:00
#*** 9.023 Collecting sentencepiece==0.***.99
#*** 9.029   Downloading sentencepiece-0.***.99-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (***.3 MB)
#*** 9.036      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***.3/***.3 MB 259.8 MB/s eta 0:00:00
#*** 9.***5 Collecting pytest==8.0.0
#*** 9.***9   Downloading pytest-8.0.0-py3-none-any.whl (334 kB)
#*** 9.***22      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 334.0/334.0 kB 3***3.5 MB/s eta 0:00:00
#*** 9.***62 Collecting flake8==7.0.0
#*** 9.***66   Downloading flake8-7.0.0-py2.py3-none-any.whl (57 kB)
#*** 9.***68      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.6/57.6 kB 247.0 MB/s eta 0:00:00
#*** 9.203 Collecting pytest-mock==3.***2.0
#*** 9.207   Downloading pytest_mock-3.***2.0-py3-none-any.whl (9.8 kB)
#*** 9.297 Collecting streamlit==***.3***.0
#*** 9.303   Downloading streamlit-***.3***.0-py2.py3-none-any.whl (8.4 MB)
#*** 9.340      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.4/8.4 MB 24***.0 MB/s eta 0:00:00
#*** 9.4***6 Collecting plotly==5.***8.0
#*** 9.42***   Downloading plotly-5.***8.0-py3-none-any.whl (***5.6 MB)
#*** 9.483      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***5.6/***5.6 MB 259.2 MB/s eta 0:00:00
#*** 9.654 Collecting aiodns>=***.***.***
#*** 9.658   Downloading aiodns-3.6.***-py3-none-any.whl (8.0 kB)
#*** ***0.43 Collecting yarl>=***.7.2
#*** ***0.44   Downloading yarl-***.22.0-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (346 kB)
#*** ***0.44      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 346.5/346.5 kB 323.7 MB/s eta 0:00:00
#*** ***0.97 Collecting cryptography>=2.6.***
#*** ***0.98   Downloading cryptography-50.0.0-cp39-abi3-manylinux_2_34_x86_64.whl (4.8 MB)
#*** ***.00      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.8/4.8 MB 268.4 MB/s eta 0:00:00
#*** ***.***0 Collecting typing-extensions>=4.4.0
#*** ***.***0   Downloading typing_extensions-4.***6.0-py3-none-any.whl (45 kB)
#*** ***.***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45.6/45.6 kB ***95.3 MB/s eta 0:00:00
#*** ***2.65 Collecting aiohttp>=3.8
#*** ***2.65   Downloading aiohttp-3.***3.5-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (***.7 MB)
#*** ***2.66      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***.7/***.7 MB 263.7 MB/s eta 0:00:00
#*** ***2.70 Collecting certifi>=20***8.***.***8
#*** ***2.70   Downloading certifi-2026.7.22-py3-none-any.whl (***36 kB)
#*** ***2.70      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***37.0/***37.0 kB 267.0 MB/s eta 0:00:00
#*** ***2.7*** Requirement already satisfied: setuptools>=60.9.0 in /usr/local/lib/python3.9/site-packages (from ccxt==4.2.34->-r requirements.txt (line 2)) (79.0.***)
#*** ***2.84 Collecting pytz>=2020.***
#*** ***2.85   Downloading pytz-2026.3.post***-py2.py3-none-any.whl (508 kB)
#*** ***2.85      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 508.3/508.3 kB 326.*** MB/s eta 0:00:00
#*** ***2.88 Collecting python-dateutil>=2.8.2
#*** ***2.88   Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)
#*** ***2.88      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 229.9/229.9 kB 3***7.9 MB/s eta 0:00:00
#*** ***2.9*** Collecting tzdata>=2022.7
#*** ***2.9***   Downloading tzdata-2026.3-py2.py3-none-any.whl (348 kB)
#*** ***2.9***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 348.2/348.2 kB 32***.5 MB/s eta 0:00:00
#*** ***3.00 Collecting urllib3<3,>=***.2***.***
#*** ***3.00   Downloading urllib3-2.6.3-py3-none-any.whl (***3*** kB)
#*** ***3.00      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***3***.6/***3***.6 kB 293.9 MB/s eta 0:00:00
#*** ***3.30 Collecting charset-normalizer<4,>=2
#*** ***3.30   Downloading charset_normalizer-3.4.9-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (2***4 kB)
#*** ***3.3***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2***4.3/2***4.3 kB 296.7 MB/s eta 0:00:00
#*** ***3.33 Collecting idna<4,>=2.5
#*** ***3.34   Downloading idna-3.***8-py3-none-any.whl (65 kB)
#*** ***3.34      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65.5/65.5 kB 258.0 MB/s eta 0:00:00
#*** ***3.39 Collecting nvidia-curand-cu***2==***0.3.2.***06
#*** ***3.39   Downloading nvidia_curand_cu***2-***0.3.2.***06-py3-none-manylinux***_x86_64.whl (56.5 MB)
#*** ***3.58      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 56.5/56.5 MB 297.6 MB/s eta 0:00:00
#*** ***3.67 Collecting nvidia-cuda-runtime-cu***2==***2.***.***05
#*** ***3.67   Downloading nvidia_cuda_runtime_cu***2-***2.***.***05-py3-none-manylinux***_x86_64.whl (823 kB)
#*** ***3.67      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 823.6/823.6 kB 3***8.8 MB/s eta 0:00:00
#*** ***3.70 Collecting jinja2
#*** ***3.70   Downloading jinja2-3.***.6-py3-none-any.whl (***34 kB)
#*** ***3.7***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***34.9/***34.9 kB 298.8 MB/s eta 0:00:00
#*** ***3.74 Collecting networkx
#*** ***3.75   Downloading networkx-3.2.***-py3-none-any.whl (***.6 MB)
#*** ***3.75      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***.6/***.6 MB 3***4.7 MB/s eta 0:00:00
#*** ***3.78 Collecting nvidia-cusolver-cu***2==***.4.5.***07
#*** ***3.79   Downloading nvidia_cusolver_cu***2-***.4.5.***07-py3-none-manylinux***_x86_64.whl (***24.2 MB)
#*** ***4.***8      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***24.2/***24.2 MB 3***7.5 MB/s eta 0:00:00
#*** ***4.34 Collecting nvidia-cuda-nvrtc-cu***2==***2.***.***05
#*** ***4.35   Downloading nvidia_cuda_nvrtc_cu***2-***2.***.***05-py3-none-manylinux***_x86_64.whl (23.7 MB)
#*** ***4.43      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 23.7/23.7 MB 3***4.2 MB/s eta 0:00:00
#*** ***4.48 Collecting nvidia-nccl-cu***2==2.***9.3
#*** ***4.48   Downloading nvidia_nccl_cu***2-2.***9.3-py3-none-manylinux***_x86_64.whl (***66.0 MB)
#*** ***5.03      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***66.0/***66.0 MB 3***0.7 MB/s eta 0:00:00
#*** ***5.25 Collecting triton==2.2.0
#*** ***5.25   Downloading triton-2.2.0-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (***67.9 MB)
#*** ***6.08      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***67.9/***67.9 MB ***99.9 MB/s eta 0:00:00
#*** ***6.29 Collecting sympy
#*** ***6.29   Downloading sympy-***.***4.0-py3-none-any.whl (6.3 MB)
#*** ***6.32      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.3/6.3 MB 298.5 MB/s eta 0:00:00
#*** ***6.36 Collecting nvidia-cublas-cu***2==***2.***.3.***
#*** ***6.37   Downloading nvidia_cublas_cu***2-***2.***.3.***-py3-none-manylinux***_x86_64.whl (4***0.6 MB)
#*** ***8.58      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4***0.6/4***0.6 MB 280.8 MB/s eta 0:00:00
#*** ***9.06 Collecting nvidia-cufft-cu***2==***.0.2.54
#*** ***9.06   Downloading nvidia_cufft_cu***2-***.0.2.54-py3-none-manylinux***_x86_64.whl (***2***.6 MB)
#*** ***9.46      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***2***.6/***2***.6 MB 3***6.6 MB/s eta 0:00:00
#*** ***9.62 Collecting nvidia-cuda-cupti-cu***2==***2.***.***05
#*** ***9.62   Downloading nvidia_cuda_cupti_cu***2-***2.***.***05-py3-none-manylinux***_x86_64.whl (***4.*** MB)
#*** ***9.67      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***4.***/***4.*** MB 3***4.0 MB/s eta 0:00:00
#*** ***9.7*** Collecting nvidia-nvtx-cu***2==***2.***.***05
#*** ***9.72   Downloading nvidia_nvtx_cu***2-***2.***.***05-py3-none-manylinux***_x86_64.whl (99 kB)
#*** ***9.72      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 99.***/99.*** kB 287.5 MB/s eta 0:00:00
#*** ***9.75 Collecting nvidia-cudnn-cu***2==8.9.2.26
#*** ***9.76   Downloading nvidia_cudnn_cu***2-8.9.2.26-py3-none-manylinux***_x86_64.whl (73***.7 MB)
#*** 22.***5      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 73***.7/73***.7 MB 3***9.9 MB/s eta 0:00:00
#*** 22.98 Collecting nvidia-cusparse-cu***2==***2.***.0.***06
#*** 22.98   Downloading nvidia_cusparse_cu***2-***2.***.0.***06-py3-none-manylinux***_x86_64.whl (***96.0 MB)
#*** 23.6***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***96.0/***96.0 MB 307.5 MB/s eta 0:00:00
#*** 23.86 Collecting filelock
#*** 23.87   Downloading filelock-3.***9.***-py3-none-any.whl (***5 kB)
#*** 23.9*** Collecting fsspec
#*** 23.9***   Downloading fsspec-2025.***0.0-py3-none-any.whl (200 kB)
#*** 23.9***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20***.0/20***.0 kB 308.5 MB/s eta 0:00:00
#*** 24.38 Collecting pillow!=8.3.*,>=5.3.0
#*** 24.38   Downloading pillow-***.3.0-cp39-cp39-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (6.6 MB)
#*** 24.4***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 300.4 MB/s eta 0:00:00
#*** 24.55 Collecting threadpoolctl>=2.0.0
#*** 24.56   Downloading threadpoolctl-3.6.0-py3-none-any.whl (***8 kB)
#*** 24.59 Collecting joblib>=***.2.0
#*** 24.60   Downloading joblib-***.5.3-py3-none-any.whl (309 kB)
#*** 24.60      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 309.***/309.*** kB 322.4 MB/s eta 0:00:00
#*** 24.96 Collecting scipy>=***.6.0
#*** 24.96   Downloading scipy-***.***3.***-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (38.6 MB)
#*** 25.09      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 38.6/38.6 MB 3***8.7 MB/s eta 0:00:00
#*** 25.90 Collecting tokenizers<0.***9,>=0.***4
#*** 25.90   Downloading tokenizers-0.***5.2-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (3.6 MB)
#*** 25.94      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.6/3.6 MB ***24.6 MB/s eta 0:00:00
#*** 25.97 Collecting packaging>=20.0
#*** 25.98   Downloading packaging-26.3-py3-none-any.whl (***29 kB)
#*** 25.98      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***30.0/***30.0 kB 28***.8 MB/s eta 0:00:00
#*** 27.***8 Collecting regex!=20***9.***2.***7
#*** 27.***8   Downloading regex-2026.***.***5-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (79*** kB)
#*** 27.***9      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 79***.3/79***.3 kB 305.4 MB/s eta 0:00:00
#*** 27.3*** Collecting huggingface-hub<***.0,>=0.***9.3
#*** 27.3***   Downloading huggingface_hub-0.36.2-py3-none-any.whl (566 kB)
#*** 27.32      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 566.4/566.4 kB 332.2 MB/s eta 0:00:00
#*** 27.64 Collecting safetensors>=0.4.***
#*** 27.65   Downloading safetensors-0.7.0-cp38-abi3-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (507 kB)
#*** 27.65      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 507.2/507.2 kB 325.4 MB/s eta 0:00:00
#*** 27.72 Collecting tqdm>=4.27
#*** 27.73   Downloading tqdm-4.70.0-py3-none-any.whl (80 kB)
#*** 27.73      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80.2/80.2 kB 278.4 MB/s eta 0:00:00
#*** 27.77 Collecting exceptiongroup>=***.0.0rc8
#*** 27.77   Downloading exceptiongroup-***.3.***-py3-none-any.whl (***6 kB)
#*** 27.78 Collecting iniconfig
#*** 27.79   Downloading iniconfig-2.***.0-py3-none-any.whl (6.0 kB)
#*** 27.8*** Collecting pluggy<2.0,>=***.3.0
#*** 27.8***   Downloading pluggy-***.6.0-py3-none-any.whl (20 kB)
#*** 27.86 Collecting tomli>=***.0.0
#*** 27.87   Downloading tomli-2.4.***-py3-none-any.whl (***4 kB)
#*** 27.89 Collecting pycodestyle<2.***2.0,>=2.***.0
#*** 27.89   Downloading pycodestyle-2.***.***-py2.py3-none-any.whl (3*** kB)
#*** 27.9*** Collecting mccabe<0.8.0,>=0.7.0
#*** 27.9***   Downloading mccabe-0.7.0-py2.py3-none-any.whl (7.3 kB)
#*** 27.94 Collecting pyflakes<3.3.0,>=3.2.0
#*** 27.94   Downloading pyflakes-3.2.0-py2.py3-none-any.whl (62 kB)
#*** 27.94      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.7/62.7 kB 263.9 MB/s eta 0:00:00
#*** 28.***0 Collecting watchdog>=2.***.5
#*** 28.***0   Downloading watchdog-6.0.0-py3-none-manylinux20***4_x86_64.whl (79 kB)
#*** 28.***0      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 79.***/79.*** kB 264.7 MB/s eta 0:00:00
#*** 28.53 Collecting protobuf<5,>=3.20
#*** 28.53   Downloading protobuf-4.25.9-cp37-abi3-manylinux20***4_x86_64.whl (295 kB)
#*** 28.53      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 295.2/295.2 kB 3***6.7 MB/s eta 0:00:00
#*** 28.63 Collecting rich<***4,>=***0.***4.0
#*** 28.64   Downloading rich-***3.9.4-py3-none-any.whl (242 kB)
#*** 28.64      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 242.4/242.4 kB 303.7 MB/s eta 0:00:00
#*** 28.66 Collecting pillow!=8.3.*,>=5.3.0
#*** 28.66   Downloading pillow-***0.4.0-cp39-cp39-manylinux_2_28_x86_64.whl (4.5 MB)
#*** 28.68      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 3***7.4 MB/s eta 0:00:00
#*** 28.7*** Collecting tenacity<9,>=8.***.0
#*** 28.72   Downloading tenacity-8.5.0-py3-none-any.whl (28 kB)
#*** 28.73 Collecting blinker<2,>=***.0.0
#*** 28.74   Downloading blinker-***.9.0-py3-none-any.whl (8.5 kB)
#*** 28.76 Collecting pydeck<***,>=0.8.0b4
#*** 28.77   Downloading pydeck-0.9.3-py2.py3-none-any.whl (***.4 MB)
#*** 28.8***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***.4/***.4 MB 3***2.5 MB/s eta 0:00:00
#*** 28.84 Collecting packaging>=20.0
#*** 28.85   Downloading packaging-23.2-py3-none-any.whl (53 kB)
#*** 28.85      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 220.8 MB/s eta 0:00:00
#*** 28.93 Collecting importlib-metadata<8,>=***.4
#*** 28.93   Downloading importlib_metadata-7.2.***-py3-none-any.whl (25 kB)
#*** 29.***6 Collecting pyarrow>=7.0
#*** 29.***7   Downloading pyarrow-2***.0.0-cp39-cp39-manylinux_2_28_x86_64.whl (42.7 MB)
#*** 29.34      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.7/42.7 MB 260.7 MB/s eta 0:00:00
#*** 29.42 Collecting validators<***,>=0.2
#*** 29.42   Downloading validators-0.35.0-py3-none-any.whl (44 kB)
#*** 29.42      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.7/44.7 kB 242.3 MB/s eta 0:00:00
#*** 29.45 Collecting altair<6,>=4.0
#*** 29.46   Downloading altair-5.5.0-py3-none-any.whl (73*** kB)
#*** 29.46      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 73***.2/73***.2 kB 337.8 MB/s eta 0:00:00
#*** 29.48 Collecting toml<2,>=0.***0.***
#*** 29.49   Downloading toml-0.***0.2-py2.py3-none-any.whl (***6 kB)
#*** 29.57 Collecting tornado<7,>=6.0.3
#*** 29.57   Downloading tornado-6.5.8-cp39-abi3-manylinux***_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (450 kB)
#*** 29.58      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 450.7/450.7 kB 332.0 MB/s eta 0:00:00
#*** 29.64 Collecting gitpython!=3.***.***9,<4,>=3.0.7
#*** 29.65   Downloading gitpython-3.***.58-py3-none-any.whl (220 kB)
#*** 29.65      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 220.2/220.2 kB 306.8 MB/s eta 0:00:00
#*** 29.68 Collecting cachetools<6,>=4.0
#*** 29.69   Downloading cachetools-5.5.2-py3-none-any.whl (***0 kB)
#*** 29.73 Collecting click<9,>=7.0
#*** 29.74   Downloading click-8.***.8-py3-none-any.whl (98 kB)
#*** 29.74      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 98.2/98.2 kB 25***.5 MB/s eta 0:00:00
#*** 29.77 Collecting tzlocal<6,>=***.***
#*** 29.77   Downloading tzlocal-5.3.***-py3-none-any.whl (***8 kB)
#*** 29.82 Collecting nvidia-nvjitlink-cu***2
#*** 29.83   Downloading nvidia_nvjitlink_cu***2-***2.9.86-py3-none-manylinux20***0_x86_64.manylinux_2_***2_x86_64.whl (39.7 MB)
#*** 29.99      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 39.7/39.7 MB 266.6 MB/s eta 0:00:00
#*** 30.40 Collecting pycares<5,>=4.9.0
#*** 30.4***   Downloading pycares-4.***.0-cp39-cp39-manylinux_2_28_x86_64.whl (643 kB)
#*** 30.4***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 643.9/643.9 kB 3***6.6 MB/s eta 0:00:00
#*** 30.45 Collecting async-timeout<6.0,>=4.0
#*** 30.45   Downloading async_timeout-5.0.***-py3-none-any.whl (6.2 kB)
#*** 30.63 Collecting frozenlist>=***.***.***
#*** 30.63   Downloading frozenlist-***.8.0-cp39-cp39-manylinux***_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (2***9 kB)
#*** 30.64      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2***9.5/2***9.5 kB 3***4.6 MB/s eta 0:00:00
#*** 30.65 Collecting aiosignal>=***.4.0
#*** 30.66   Downloading aiosignal-***.4.0-py3-none-any.whl (7.5 kB)
#*** 3***.30 Collecting multidict<7.0,>=4.5
#*** 3***.30   Downloading multidict-6.7.***-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (240 kB)
#*** 3***.3***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 240.3/240.3 kB 306.7 MB/s eta 0:00:00
#*** 3***.35 Collecting aiohappyeyeballs>=2.5.0
#*** 3***.35   Downloading aiohappyeyeballs-2.6.***-py3-none-any.whl (***5 kB)
#*** 3***.5*** Collecting propcache>=0.2.0
#*** 3***.5***   Downloading propcache-0.4.***-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (***97 kB)
#*** 3***.5***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***97.2/***97.2 kB 289.5 MB/s eta 0:00:00
#*** 3***.54 Collecting attrs>=***7.3.0
#*** 3***.54   Downloading attrs-26.***.0-py3-none-any.whl (67 kB)
#*** 3***.55      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 67.5/67.5 kB 257.8 MB/s eta 0:00:00
#*** 3***.68 Collecting narwhals>=***.***4.2
#*** 3***.68   Downloading narwhals-2.2***.0-py3-none-any.whl (45*** kB)
#*** 3***.68      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 45***.9/45***.9 kB 329.*** MB/s eta 0:00:00
#*** 3***.74 Collecting jsonschema>=3.0
#*** 3***.74   Downloading jsonschema-4.25.***-py3-none-any.whl (90 kB)
#*** 3***.74      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 90.0/90.0 kB 263.0 MB/s eta 0:00:00
#*** 32.07 Collecting cffi>=2.0.0
#*** 32.08   Downloading cffi-2.0.0-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.whl (2***6 kB)
#*** 32.08      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2***6.5/2***6.5 kB 285.7 MB/s eta 0:00:00
#*** 32.***4 Collecting gitdb<5,>=4.0.***
#*** 32.***4   Downloading gitdb-4.0.***2-py3-none-any.whl (62 kB)
#*** 32.***4      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.8/62.8 kB 220.7 MB/s eta 0:00:00
#*** 32.37 Collecting hf-xet<2.0.0,>=***.***.3
#*** 32.38   Downloading hf_xet-***.6.0-cp38-abi3-manylinux20***4_x86_64.manylinux_2_***7_x86_64.whl (4.5 MB)
#*** 32.40      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 268.3 MB/s eta 0:00:00
#*** 32.57 Collecting zipp>=0.5
#*** 32.57   Downloading zipp-3.23.***-py3-none-any.whl (***0 kB)
#*** 32.80 Collecting MarkupSafe>=2.0
#*** 32.80   Downloading markupsafe-3.0.3-cp39-cp39-manylinux20***4_x86_64.manylinux_2_***7_x86_64.manylinux_2_28_x86_64.whl (20 kB)
#*** 32.83 Collecting six>=***.5
#*** 32.84   Downloading six-***.***7.0-py2.py3-none-any.whl (*** kB)
#*** 32.89 Collecting pygments<3.0.0,>=2.***3.0
#*** 32.90   Downloading pygments-2.20.0-py3-none-any.whl (***.2 MB)
#*** 32.90      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***.2/***.2 MB 3***4.5 MB/s eta 0:00:00
#*** 32.94 Collecting markdown-it-py>=2.2.0
#*** 32.95   Downloading markdown_it_py-3.0.0-py3-none-any.whl (87 kB)
#*** 32.95      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 87.5/87.5 kB 285.5 MB/s eta 0:00:00
#*** 33.28 Collecting mpmath<***.4,>=***.***.0
#*** 33.28   Downloading mpmath-***.3.0-py3-none-any.whl (536 kB)
#*** 33.29      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 536.2/536.2 kB 3***3.*** MB/s eta 0:00:00
#*** 33.36 Collecting pycparser
#*** 33.36   Downloading pycparser-2.23-py3-none-any.whl (***8 kB)
#*** 33.37      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ***8.***/***8.*** kB 255.6 MB/s eta 0:00:00
#*** 33.40 Collecting smmap<6,>=3.0.***
#*** 33.4***   Downloading smmap-5.0.3-py3-none-any.whl (24 kB)
#*** 34.40 Collecting rpds-py>=0.7.***
#*** 34.4***   Downloading rpds_py-0.27.***-cp39-cp39-manylinux_2_***7_x86_64.manylinux20***4_x86_64.whl (384 kB)
#*** 34.4***      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 384.4/384.4 kB 286.9 MB/s eta 0:00:00
#*** 34.43 Collecting jsonschema-specifications>=2023.03.6
#*** 34.44   Downloading jsonschema_specifications-2025.9.***-py3-none-any.whl (***8 kB)
#*** 34.48 Collecting referencing>=0.28.4
#*** 34.49   Downloading referencing-0.36.2-py3-none-any.whl (26 kB)
#*** 34.53 Collecting mdurl~=0.***
#*** 34.53   Downloading mdurl-0.***.2-py3-none-any.whl (***0.0 kB)
#*** 36.07 Installing collected packages: sentencepiece, pytz, mpmath, zipp, watchdog, validators, urllib3, tzlocal, tzdata, typing-extensions, tqdm, tornado, tomli, toml, threadpoolctl, tenacity, sympy, smmap, six, safetensors, rpds-py, regex, pyyaml, python-dotenv, pygments, pyflakes, pycparser, pycodestyle, pyarrow, protobuf, propcache, pluggy, pillow, packaging, nvidia-nvtx-cu***2, nvidia-nvjitlink-cu***2, nvidia-nccl-cu***2, nvidia-curand-cu***2, nvidia-cufft-cu***2, nvidia-cuda-runtime-cu***2, nvidia-cuda-nvrtc-cu***2, nvidia-cuda-cupti-cu***2, nvidia-cublas-cu***2, numpy, networkx, narwhals, mdurl, mccabe, MarkupSafe, joblib, iniconfig, idna, hf-xet, fsspec, frozenlist, filelock, click, charset-normalizer, certifi, cachetools, blinker, attrs, async-timeout, aiohappyeyeballs, triton, scipy, requests, referencing, python-dateutil, plotly, nvidia-cusparse-cu***2, nvidia-cudnn-cu***2, multidict, markdown-it-py, jinja2, importlib-metadata, gitdb, flake8, exceptiongroup, cffi, aiosignal, yarl, scikit-learn, rich, pytest, pydeck, pycares, pandas, nvidia-cusolver-cu***2, jsonschema-specifications, huggingface-hub, gitpython, cryptography, torch, tokenizers, pytest-mock, jsonschema, aiohttp, aiodns, transformers, torchvision, ccxt, altair, streamlit
#*** 36.6***   WARNING: The script watchmedo is installed in '/root/.local/bin' which is not on PATH.
#*** 36.6***   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 36.9***   WARNING: The script tqdm is installed in '/root/.local/bin' which is not on PATH.
#*** 36.9***   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 42.43   WARNING: The script isympy is installed in '/root/.local/bin' which is not on PATH.
#*** 42.43   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 42.65   WARNING: The script dotenv is installed in '/root/.local/bin' which is not on PATH.
#*** 42.65   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 43.34   WARNING: The script pygmentize is installed in '/root/.local/bin' which is not on PATH.
#*** 43.34   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 43.39   WARNING: The script pyflakes is installed in '/root/.local/bin' which is not on PATH.
#*** 43.39   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 43.54   WARNING: The script pycodestyle is installed in '/root/.local/bin' which is not on PATH.
#*** 43.54   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 55.26   WARNING: The script f2py is installed in '/root/.local/bin' which is not on PATH.
#*** 55.26   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 56.89   WARNING: The script idna is installed in '/root/.local/bin' which is not on PATH.
#*** 56.89   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 57.2***   WARNING: The script normalizer is installed in '/root/.local/bin' which is not on PATH.
#*** 57.2***   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 80.07   WARNING: The script markdown-it is installed in '/root/.local/bin' which is not on PATH.
#*** 80.07   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 80.25   WARNING: The script flake8 is installed in '/root/.local/bin' which is not on PATH.
#*** 80.25   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 82.52   WARNING: The scripts py.test and pytest are installed in '/root/.local/bin' which is not on PATH.
#*** 82.52   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** 89.38   WARNING: The scripts hf, huggingface-cli and tiny-agents are installed in '/root/.local/bin' which is not on PATH.
#*** 89.38   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** ***05.9   WARNING: The scripts convert-caffe2-to-onnx, convert-onnx-to-caffe2 and torchrun are installed in '/root/.local/bin' which is not on PATH.
#*** ***05.9   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** ***06.***   WARNING: The script jsonschema is installed in '/root/.local/bin' which is not on PATH.
#*** ***06.***   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** ***.0   WARNING: The script transformers-cli is installed in '/root/.local/bin' which is not on PATH.
#*** ***.0   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** ***4.5   WARNING: The script streamlit is installed in '/root/.local/bin' which is not on PATH.
#*** ***4.5   Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
#*** ***4.6 Successfully installed MarkupSafe-3.0.3 aiodns-3.6.*** aiohappyeyeballs-2.6.*** aiohttp-3.***3.5 aiosignal-***.4.0 altair-5.5.0 async-timeout-5.0.*** attrs-26.***.0 blinker-***.9.0 cachetools-5.5.2 ccxt-4.2.34 certifi-2026.7.22 cffi-2.0.0 charset-normalizer-3.4.9 click-8.***.8 cryptography-50.0.0 exceptiongroup-***.3.*** filelock-3.***9.*** flake8-7.0.0 frozenlist-***.8.0 fsspec-2025.***0.0 gitdb-4.0.***2 gitpython-3.***.58 hf-xet-***.6.0 huggingface-hub-0.36.2 idna-3.***8 importlib-metadata-7.2.*** iniconfig-2.***.0 jinja2-3.***.6 joblib-***.5.3 jsonschema-4.25.*** jsonschema-specifications-2025.9.*** markdown-it-py-3.0.0 mccabe-0.7.0 mdurl-0.***.2 mpmath-***.3.0 multidict-6.7.*** narwhals-2.2***.0 networkx-3.2.*** numpy-***.26.3 nvidia-cublas-cu***2-***2.***.3.*** nvidia-cuda-cupti-cu***2-***2.***.***05 nvidia-cuda-nvrtc-cu***2-***2.***.***05 nvidia-cuda-runtime-cu***2-***2.***.***05 nvidia-cudnn-cu***2-8.9.2.26 nvidia-cufft-cu***2-***.0.2.54 nvidia-curand-cu***2-***0.3.2.***06 nvidia-cusolver-cu***2-***.4.5.***07 nvidia-cusparse-cu***2-***2.***.0.***06 nvidia-nccl-cu***2-2.***9.3 nvidia-nvjitlink-cu***2-***2.9.86 nvidia-nvtx-cu***2-***2.***.***05 packaging-23.2 pandas-2.2.0 pillow-***0.4.0 plotly-5.***8.0 pluggy-***.6.0 propcache-0.4.*** protobuf-4.25.9 pyarrow-2***.0.0 pycares-4.***.0 pycodestyle-2.***.*** pycparser-2.23 pydeck-0.9.3 pyflakes-3.2.0 pygments-2.20.0 pytest-8.0.0 pytest-mock-3.***2.0 python-dateutil-2.9.0.post0 python-dotenv-***.0.*** pytz-2026.3.post*** pyyaml-6.0.*** referencing-0.36.2 regex-2026.***.***5 requests-2.3***.0 rich-***3.9.4 rpds-py-0.27.*** safetensors-0.7.0 scikit-learn-***.4.0 scipy-***.***3.*** sentencepiece-0.***.99 six-***.***7.0 smmap-5.0.3 streamlit-***.3***.0 sympy-***.***4.0 tenacity-8.5.0 threadpoolctl-3.6.0 tokenizers-0.***5.2 toml-0.***0.2 tomli-2.4.*** torch-2.2.0 torchvision-0.***7.0 tornado-6.5.8 tqdm-4.70.0 transformers-4.37.2 triton-2.2.0 typing-extensions-4.***6.0 tzdata-2026.3 tzlocal-5.3.*** urllib3-2.6.3 validators-0.35.0 watchdog-6.0.0 yarl-***.22.0 zipp-3.23.***
#*** ***4.6 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
#*** DONE ***9.***s

#***2 [stage-*** 4/6] COPY --from=builder /root/.local /home/nexus/.local
#***2 DONE 29.6s

#***3 [stage-*** 5/6] COPY . .
#***3 DONE 0.0s

#***4 [stage-*** 6/6] RUN chown -R nexus:nexus /app
#***4 DONE 0.2s

#***5 exporting to image
#***5 exporting layers
#***5 exporting layers 25.6s done
#***5 writing image sha256:5225d***26725d7e0c932735f6f6ed***4465630dd36e2***5***a5a3d8f42fe2d6fea80 done
#***5 naming to docker.io/library/nexus-smc-engine:latest done
#***5 DONE 25.6s

 *** warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 2)
Build successful for TechSolute architecture.
Error: The operation was canceled."""
Implementation of the FeatureEngineProtocol.
Transforms raw MT5 dictionaries into a strongly-typed FeatureSnapshot.
"""

import pandas as pd
from typing import List
from datetime import datetime, timezone

from app.core.interfaces import FeatureEngineProtocol
from app.domain.models import FeatureSnapshot
from app.features.indicators import (
    calculate_ema,
    calculate_rsi,
    calculate_atr,
    calculate_bollinger_bands_width
)


class PandasFeatureEngine(FeatureEngineProtocol):
    """
    Computes technical features deterministically.
    Version: 1.0.0
    """
    FEATURE_VERSION = "1.0.0"

    def compute_features(self, symbol: str, timeframe: str, candles: List[dict]) -> FeatureSnapshot:
        if not candles or len(candles) < 50:
            raise ValueError(f"Insufficient data for feature calculation. Required: 50, Got: {len(candles)}")

        # Convert to DataFrame
        df = pd.DataFrame(candles)
        
        # Ensure timestamp is parsed properly. MT5 returns unix timestamps in seconds.
        if "time" in df.columns:
            df["timestamp"] = pd.to_datetime(df["time"], unit="s", utc=True)
        else:
            raise ValueError("Candle data missing 'time' key.")

        # Calculate Indicators
        df["ema_20"] = calculate_ema(df["close"], 20)
        df["ema_50"] = calculate_ema(df["close"], 50)
        df["rsi_14"] = calculate_rsi(df["close"], 14)
        df["atr_14"] = calculate_atr(df["high"], df["low"], df["close"], 14)
        df["bb_width_20"] = calculate_bollinger_bands_width(df["close"], 20, 2.0)
        
        # Trend Proxies
        df["trend_distance"] = (df["ema_20"] - df["ema_50"]) / df["ema_50"]
        
        # Extract the latest fully calculated row (index -1)
        # We assume the caller ensures the last candle provided is a closed candle
        # or it represents the instantaneous state at tick time.
        latest = df.iloc[-1]

        # Extract features into a dictionary, dropping NaNs or returning safe defaults
        features = {
            "ema_20": float(latest["ema_20"]),
            "ema_50": float(latest["ema_50"]),
            "rsi_14": float(latest["rsi_14"]),
            "atr_14": float(latest["atr_14"]),
            "bb_width_20": float(latest["bb_width_20"]),
            "trend_distance": float(latest["trend_distance"]),
            "close": float(latest["close"]),
            "volume": float(latest["tick_volume"]) if "tick_volume" in df.columns else 0.0
        }

        # Check for invalid math (NaNs) due to insufficient lookback just in case
        if any(pd.isna(v) for v in features.values()):
            raise ValueError("Feature calculation resulted in NaN values. Check lookback periods.")

        return FeatureSnapshot(
            timestamp=latest["timestamp"].to_pydatetime(),
            symbol=symbol,
            timeframe=timeframe,
            features=features,
            feature_version=self.FEATURE_VERSION
        )