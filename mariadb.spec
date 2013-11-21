# In f20+ use unversioned docdirs, otherwise the old versioned one
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

# TokuDB engine is now part of MariaDB, but it is available only for x86_64;
# variable tokudb allows to build with TokuDB storage engine
%bcond_with tokudb

Name: mariadb
Version: 5.5.33a
Release: 6%{?dist}

Summary: A community developed branch of MySQL
Group: Applications/Databases
URL: http://mariadb.org
# Exceptions allow client libraries to be linked with most open source SW,
# not only GPL code.  See README.mysql-license
# Some innobase code from Percona and Google is under BSD license
# Some code related to test-suite is under LGPLv2
License: GPLv2 with exceptions and LGPLv2 and BSD

# Regression tests take a long time, you can skip 'em with this
%{!?runselftest:%global runselftest 1}

Source0: http://ftp.osuosl.org/pub/mariadb/mariadb-%{version}/kvm-tarbake-jaunty-x86/mariadb-%{version}.tar.gz
Source3: my.cnf
Source5: my_config.h
Source6: README.mysql-docs
Source7: README.mysql-license
Source8: libmysql.version
Source9: mysql-embedded-check.c
Source11: mysql.init
Source14: rh-skipped-tests-base.list
Source15: rh-skipped-tests-arm.list
# Working around perl dependency checking bug in rpm FTTB. Remove later.
Source999: filter-requires-mysql.sh

# Comments for these patches are in the patch files.
Patch1: mariadb-errno.patch
Patch2: mariadb-strmov.patch
Patch3: mariadb-install-test.patch
Patch4: mariadb-expired-certs.patch
Patch5: mariadb-versioning.patch
Patch6: mariadb-dubious-exports.patch
Patch7: mariadb-s390-tsc.patch
Patch8: mariadb-logrotate.patch
Patch9: mariadb-cipherspec.patch
Patch10: mariadb-file-contents.patch
Patch11: mariadb-string-overflow.patch
Patch12: mariadb-dh1024.patch
Patch14: mariadb-basedir.patch
Patch17: mariadb-covscan-signexpr.patch
Patch18: mariadb-covscan-stroverflow.patch
Patch20: mariadb-cmakehostname.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl, readline-devel, openssl-devel
BuildRequires: cmake, ncurses-devel, zlib-devel, libaio-devel
%if 0%{?rhel}>=6 || 0%{?fedora}
BuildRequires: systemtap-sdt-devel
%endif
# make test requires time and ps
BuildRequires: time procps
# auth_pam.so plugin will be build if pam-devel is installed
BuildRequires: pam-devel
# perl modules needed to run regression tests
BuildRequires: perl(Socket), perl(Time::HiRes)
BuildRequires: perl(Data::Dumper), perl(Test::More), perl(Env)

Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: grep, fileutils, bash
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

# MariaDB replaces mysql packages
Provides: mysql = %{version}-%{release}
Provides: mysql%{?_isa} = %{version}-%{release}
Provides: real-%{name} = %{version}-%{release}
Provides: real-%{name}%{?_isa} = %{version}-%{release}
Conflicts: real-mysql
# mysql-cluster used to be built from this SRPM, but no more
Obsoletes: mysql-cluster < 5.1.44
 
# When rpm 4.9 is universal, this could be cleaned up:
%global __perl_requires %{SOURCE999}
%global __perllib_requires %{SOURCE999}

# By default, patch(1) creates backup files when chunks apply with offsets.
# Turn that off to ensure such files don't get included in RPMs (cf bz#884755).
%global _default_patch_flags --no-backup-if-mismatch

%description
MariaDB is a community developed branch of MySQL.
MariaDB is a multi-user, multi-threaded SQL database server.
It is a client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. The base package
contains the standard MariaDB/MySQL client programs and generic MySQL files.

%package libs

Summary: The shared libraries required for MariaDB/MySQL clients
Group: Applications/Databases
Requires: /sbin/ldconfig
Provides: mysql-libs = %{version}-%{release}
Provides: mysql-libs%{?_isa} = %{version}-%{release}
Provides: real-%{name}-libs = %{version}-%{release}
Provides: real-%{name}-libs%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-libs

%description libs
The mariadb-libs package provides the essential shared libraries for any 
MariaDB/MySQL client program or interface. You will need to install this
package to use any other MariaDB package or any clients that need to connect
to a MariaDB/MySQL server. MariaDB is a community developed branch of MySQL.

%package server

Summary: The MariaDB server and related files
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: sh-utils
Requires(pre): /usr/sbin/useradd
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
# mysqlhotcopy needs DBI/DBD support
Requires: perl-DBI, perl-DBD-MySQL
Conflicts: MySQL-server
Provides: mysql-server = %{version}-%{release}
Provides: mysql-server%{?_isa} = %{version}-%{release}
Provides: real-%{name}-server = %{version}-%{release}
Provides: real-%{name}-server%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-server

%description server
MariaDB is a multi-user, multi-threaded SQL database server. It is a
client/server implementation consisting of a server daemon (mysqld)
and many different client programs and libraries. This package contains
the MariaDB server and some accompanying files and directories.
MariaDB is a community developed branch of MySQL.

%package devel

Summary: Files for development of MariaDB/MySQL applications
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: openssl-devel%{?_isa}
Conflicts: MySQL-devel
Provides: mysql-devel = %{version}-%{release}
Provides: mysql-devel%{?_isa} = %{version}-%{release}
Provides: real-%{name}-devel = %{version}-%{release}
Provides: real-%{name}-devel%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-devel

%description devel
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains the libraries and header files that are needed for
developing MariaDB/MySQL client applications.
MariaDB is a community developed branch of MySQL.

%package embedded

Summary: MariaDB as an embeddable library
Group: Applications/Databases
Requires: /sbin/ldconfig
Provides: mysql-embedded = %{version}-%{release}
Provides: mysql-embedded%{?_isa} = %{version}-%{release}
Provides: real-%{name}-embedded = %{version}-%{release}
Provides: real-%{name}-embedded%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-embedded

%description embedded
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains a version of the MariaDB server that can be embedded
into a client application instead of running as a separate process.
MariaDB is a community developed branch of MySQL.

%package embedded-devel

Summary: Development files for MariaDB as an embeddable library
Group: Applications/Databases
Requires: real-%{name}-embedded%{?_isa} = %{version}-%{release}
Requires: real-%{name}-devel%{?_isa} = %{version}-%{release}
Provides: mysql-embedded-devel = %{version}-%{release}
Provides: mysql-embedded-devel%{?_isa} = %{version}-%{release}
Provides: real-%{name}-embedded-devel = %{version}-%{release}
Provides: real-%{name}-embedded-devel%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-embedded-devel

%description embedded-devel
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains files needed for developing and testing with
the embedded version of the MariaDB server.
MariaDB is a community developed branch of MySQL.

%package bench

Summary: MariaDB benchmark scripts and data
Group: Applications/Databases
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Conflicts: MySQL-bench
Provides: mysql-bench = %{version}-%{release}
Provides: mysql-bench%{?_isa} = %{version}-%{release}
Provides: real-%{name}-bench = %{version}-%{release}
Provides: real-%{name}-bench%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-bench

%description bench
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains benchmark scripts and data for use when benchmarking
MariaDB.
MariaDB is a community developed branch of MySQL.

%package test

Summary: The test suite distributed with MariaD
Group: Applications/Databases
Requires: perl(Socket), perl(Time::HiRes)
Requires: perl(Data::Dumper), perl(Test::More), perl(Env)
Requires: real-%{name}%{?_isa} = %{version}-%{release}
Requires: real-%{name}-libs%{?_isa} = %{version}-%{release}
Requires: real-%{name}-server%{?_isa} = %{version}-%{release}
Conflicts: MySQL-test
Provides: mysql-test = %{version}-%{release}
Provides: mysql-test%{?_isa} = %{version}-%{release}
Provides: real-%{name}-test  = %{version}-%{release}
Provides: real-%{name}-test%{?_isa} = %{version}-%{release}
Conflicts: real-mysql-test

%description test
MariaDB is a multi-user, multi-threaded SQL database server. This
package contains the regression test suite distributed with
the MariaDB sources.
MariaDB is a community developed branch of MySQL.

%prep
%setup -q -n mariadb-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch14 -p1
%patch17 -p1
%patch18 -p1
%patch20 -p1

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# upstream has fallen down badly on symbol versioning, do it ourselves
cp -p %{SOURCE8} libmysql/libmysql.version

# generate a list of tests that fail, but are not disabled by upstream
cat %{SOURCE14} > mysql-test/rh-skipped-tests.list
# disable some tests failing on ARM architectures
%ifarch %{arm}
cat %{SOURCE15} >> mysql-test/rh-skipped-tests.list
%endif
# disable some tests failing on ppc and s390
%ifarch ppc ppc64 ppc64p7 s390 s390x
echo "main.gis-precise : rhbz#906367" >> mysql-test/rh-skipped-tests.list
%endif

%build

# fail quickly and obviously if user tries to build as root
%if %runselftest
	if [ x"`id -u`" = x0 ]; then
		echo "mariadb's regression tests fail if run as root."
		echo "If you really need to build the RPM as root, use"
		echo "--define='runselftest 0' to skip the regression tests."
		exit 1
	fi
%endif

CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# force PIC mode so that we can build libmysqld.so
CFLAGS="$CFLAGS -fPIC"
# gcc seems to have some bugs on sparc as of 4.4.1, back off optimization
# submitted as bz #529298
%ifarch sparc sparcv9 sparc64
CFLAGS=`echo $CFLAGS| sed -e "s|-O2|-O1|g" `
%endif
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS

# The INSTALL_xxx macros have to be specified relative to CMAKE_INSTALL_PREFIX
# so we can't use %%{_datadir} and so forth here.

cmake . -DBUILD_CONFIG=mysql_release \
	-DFEATURE_SET="community" \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DINSTALL_LAYOUT=RPM \
	-DCMAKE_INSTALL_PREFIX="%{_prefix}" \
%if 0%{?fedora} >= 20
	-DINSTALL_DOCDIR=share/doc/mariadb \
	-DINSTALL_DOCREADMEDIR=share/doc/mariadb \
%else
	-DINSTALL_DOCDIR=share/doc/%{name}-%{version} \
	-DINSTALL_DOCREADMEDIR=share/doc/%{name}-%{version} \
%endif
	-DINSTALL_INCLUDEDIR=include/mysql \
	-DINSTALL_INFODIR=share/info \
	-DINSTALL_LIBDIR="%{_lib}/mysql" \
	-DINSTALL_MANDIR=share/man \
	-DINSTALL_MYSQLSHAREDIR=share/%{name} \
	-DINSTALL_MYSQLTESTDIR=share/mysql-test \
	-DINSTALL_PLUGINDIR="%{_lib}/mysql/plugin" \
	-DWITHOUT_DYNAMIC_PLUGINS=ON \
	-DINSTALL_SBINDIR=libexec \
	-DINSTALL_SCRIPTDIR=bin \
	-DINSTALL_SQLBENCHDIR=share \
	-DINSTALL_SUPPORTFILESDIR=share/mysql \
	-DMYSQL_DATADIR="%{_localstatedir}/lib/mysql" \
	-DMYSQL_UNIX_ADDR="%{_localstatedir}/lib/mysql/mysql.sock" \
	-DENABLED_LOCAL_INFILE=ON \
%if 0%{?rhel}>=6 || 0%{?fedora}
	-DENABLE_DTRACE=ON \
%endif
	-DWITH_EMBEDDED_SERVER=ON \
	-DWITH_READLINE=ON \
	-DWITH_SSL=system \
	-DWITH_ZLIB=system \
	-DWITH_JEMALLOC=no \
%{!?with_tokudb:	-DWITHOUT_TOKUDB=ON}\
	-DTMPDIR=%{_localstatedir}/tmp \
	-DWITH_MYSQLD_LDFLAGS="-Wl,-z,relro,-z,now"

make %{?_smp_mflags} VERBOSE=1

# debuginfo extraction scripts fail to find source files in their real
# location -- satisfy them by copying these files into location, which
# is expected by scripts
for e in innobase xtradb ; do
  for f in pars0grm.c pars0grm.y pars0lex.l lexyy.c ; do
    cp -p "storage/$e/pars/$f" "storage/$e/$f"
  done
done

%check
%if %runselftest
  # hack to let 32- and 64-bit tests run concurrently on same build machine
  case `uname -m` in
    ppc64 | ppc64p7 | s390x | x86_64 | sparc64 )
      MTR_BUILD_THREAD=7
      ;;
    *)
      MTR_BUILD_THREAD=11
      ;;
  esac
  export MTR_BUILD_THREAD
  export MTR_PARALLEL=1

  make test VERBOSE=1

  # The cmake build scripts don't provide any simple way to control the
  # options for mysql-test-run, so ignore the make target and just call it
  # manually.  Nonstandard options chosen are:
  # --force to continue tests after a failure
  # no retries please
  # test SSL with --ssl
  # skip tests that are listed in rh-skipped-tests.list
  # avoid redundant test runs with --binlog-format=mixed
  # increase timeouts to prevent unwanted failures during mass rebuilds
  (
    cd mysql-test
    perl ./mysql-test-run.pl --force --retry=0 --ssl \
	--skip-test-list=rh-skipped-tests.list \
	--suite-timeout=720 --testcase-timeout=30 \
	--mysqld=--binlog-format=mixed --force-restart \
	--shutdown-timeout=60 
    # cmake build scripts will install the var cruft if left alone :-(
    rm -rf var
  ) 
%endif

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT VERBOSE=1 install

# List the installed tree for RPM package maintenance purposes.
find $RPM_BUILD_ROOT -print | sed "s|^$RPM_BUILD_ROOT||" | sort > ROOTFILES

# multilib header hacks
# we only apply this to known Red Hat multilib arches, per bug #181335
case `uname -i` in
  i386 | x86_64 | ppc | ppc64 | ppc64p7 | s390 | s390x | sparc | sparc64 | aarch64 )
    mv $RPM_BUILD_ROOT%{_includedir}/mysql/my_config.h $RPM_BUILD_ROOT%{_includedir}/mysql/my_config_`uname -i`.h
    mv $RPM_BUILD_ROOT%{_includedir}/mysql/private/config.h $RPM_BUILD_ROOT%{_includedir}/mysql/private/my_config_`uname -i`.h
    install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/
    install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/private/config.h
    ;;
  arm* )
    mv $RPM_BUILD_ROOT%{_includedir}/mysql/my_config.h $RPM_BUILD_ROOT%{_includedir}/mysql/my_config_arm.h
    mv $RPM_BUILD_ROOT%{_includedir}/mysql/private/config.h $RPM_BUILD_ROOT%{_includedir}/mysql/private/my_config_arm.h
    install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/
    install -p -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_includedir}/mysql/private/config.h
    ;;
  *)
    ;;
esac

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' \
	${RPM_BUILD_ROOT}%{_bindir}/mysql_config >mysql_config.tmp
cp -p -f mysql_config.tmp ${RPM_BUILD_ROOT}%{_bindir}/mysql_config
chmod 755 ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

# install INFO_SRC, INFO_BIN into libdir (upstream thinks these are doc files,
# but that's pretty wacko --- see also mariadb-file-contents.patch)
mv ${RPM_BUILD_ROOT}%{_pkgdocdir}/INFO_SRC ${RPM_BUILD_ROOT}%{_libdir}/mysql/
mv ${RPM_BUILD_ROOT}%{_pkgdocdir}/INFO_BIN ${RPM_BUILD_ROOT}%{_libdir}/mysql/

mkdir -p $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/mysqld.log

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/mysqld
install -m 0755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/mysql

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -p -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/my.cnf

# install init script for handling server startup
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -p -m 755 %{SOURCE11} ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d/mysqld

# Fix scripts for multilib safety
mv ${RPM_BUILD_ROOT}%{_bindir}/mysql_config ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysql_config
touch ${RPM_BUILD_ROOT}%{_bindir}/mysql_config

mv ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug ${RPM_BUILD_ROOT}%{_libdir}/mysql/mysqlbug
touch ${RPM_BUILD_ROOT}%{_bindir}/mysqlbug

# Remove libmysqld.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqld.a

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so*
ln -s libmysqlclient.so ${RPM_BUILD_ROOT}%{_libdir}/mysql/libmysqlclient_r.so
 
# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process ${RPM_BUILD_ROOT}%{_bindir}
ln -s ../../../../../bin/my_safe_process ${RPM_BUILD_ROOT}%{_datadir}/mysql-test/lib/My/SafeProcess/my_safe_process

# should move this to /etc/ ?
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mysql_embedded
rm -f ${RPM_BUILD_ROOT}%{_libdir}/mysql/*.a
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/binary-configure
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/magic
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/ndb-config-2-node.ini
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql.server
rm -f ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysqld_multi.server
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-stress-test.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/mysql-test-run.pl.1*
rm -f ${RPM_BUILD_ROOT}%{_bindir}/mytop

# put logrotate script where it needs to be
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mv ${RPM_BUILD_ROOT}%{_datadir}/mysql/mysql-log-rotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mysqld
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/mysqld

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/mysql" > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

# copy additional docs into build tree so %%doc will find them
cp -p %{SOURCE6} README.mysql-docs
cp -p %{SOURCE7} README.mysql-license

# install the list of skipped tests to be available for user runs
install -m 0644 mysql-test/rh-skipped-tests.list ${RPM_BUILD_ROOT}%{_datadir}/mysql-test

# remove unneeded RHEL-4 SELinux stuff
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mysql/SELinux/

# remove SysV init script
rm -f ${RPM_BUILD_ROOT}%{_sysconfdir}/init.d/mysql

# remove duplicate logrotate script
rm -f ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/mysql

# remove solaris files
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/mysql/solaris/

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/update-alternatives --install %{_bindir}/mysql_config \
	mysql_config %{_libdir}/mysql/mysql_config %{__isa_bits}

%pre server
/usr/sbin/groupadd -g 27 -o -r mysql >/dev/null 2>&1 || :
/usr/sbin/useradd -M -N -g mysql -o -r -d %{_localstatedir}/lib/mysql -s /bin/bash \
	-c "MariaDB Server" -u 27 mysql >/dev/null 2>&1 || :

%post libs -p /sbin/ldconfig

%post server
if [ $1 = 1 ]; then
    # Initial installation
    /sbin/chkconfig --add mysqld
fi
/bin/chmod 0755 %{_localstatedir}/lib/mysql
/bin/touch %{_localstatedir}/log/mysqld.log

%{_sbindir}/update-alternatives --install %{_bindir}/mysqlbug \
	mysqlbug %{_libdir}/mysql/mysqlbug %{__isa_bits}

%post embedded -p /sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove mysql_config %{_libdir}/mysql/mysql_config
fi

%preun server
if [ $1 = 0 ]; then
    # Package removal, not upgrade
    /sbin/service mysqld stop >/dev/null 2>&1
    /sbin/chkconfig --del mysqld
fi

%postun libs -p /sbin/ldconfig

%postun server
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove mysqlbug %{_libdir}/mysql/mysqlbug
fi
if [ $1 -ge 1 ]; then
    # Package upgrade, not uninstall
    /sbin/service mysqld condrestart >/dev/null 2>&1 || :
fi

%postun embedded -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README COPYING COPYING.LESSER README.mysql-license
%doc storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
%doc README.mysql-docs

%{_bindir}/msql2mysql
%{_bindir}/mysql
%ghost %{_bindir}/mysql_config
%{_bindir}/mysql_find_rows
%{_bindir}/mysql_waitpid
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysqldump
%{?with_tokudb:%{_bindir}/tokuftdump}
%{_bindir}/mysqlimport
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/my_print_defaults
%{_bindir}/aria_chk
%{_bindir}/aria_dump_log
%{_bindir}/aria_ftdump
%{_bindir}/aria_pack
%{_bindir}/aria_read_log

%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysql_config.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql_fix_privilege_tables.1*
%{_mandir}/man8/mysqlmanager.8*

%{_libdir}/mysql/mysql_config
%config(noreplace) %{_sysconfdir}/my.cnf.d/client.cnf

%files libs
%defattr(-,root,root)
%doc README COPYING COPYING.LESSER README.mysql-license
%doc storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
# although the default my.cnf contains only server settings, we put it in the
# libs package because it can be used for client settings too.
%config(noreplace) %{_sysconfdir}/my.cnf
%config(noreplace) %{_sysconfdir}/my.cnf.d/mysql-clients.cnf
%dir %{_sysconfdir}/my.cnf.d
%dir %{_libdir}/mysql
%{_libdir}/mysql/libmysqlclient.so.*
%{_sysconfdir}/ld.so.conf.d/*

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/english
%lang(cs) %{_datadir}/%{name}/czech
%lang(da) %{_datadir}/%{name}/danish
%lang(nl) %{_datadir}/%{name}/dutch
%lang(et) %{_datadir}/%{name}/estonian
%lang(fr) %{_datadir}/%{name}/french
%lang(de) %{_datadir}/%{name}/german
%lang(el) %{_datadir}/%{name}/greek
%lang(hu) %{_datadir}/%{name}/hungarian
%lang(it) %{_datadir}/%{name}/italian
%lang(ja) %{_datadir}/%{name}/japanese
%lang(ko) %{_datadir}/%{name}/korean
%lang(no) %{_datadir}/%{name}/norwegian
%lang(no) %{_datadir}/%{name}/norwegian-ny
%lang(pl) %{_datadir}/%{name}/polish
%lang(pt) %{_datadir}/%{name}/portuguese
%lang(ro) %{_datadir}/%{name}/romanian
%lang(ru) %{_datadir}/%{name}/russian
%lang(sr) %{_datadir}/%{name}/serbian
%lang(sk) %{_datadir}/%{name}/slovak
%lang(es) %{_datadir}/%{name}/spanish
%lang(sv) %{_datadir}/%{name}/swedish
%lang(uk) %{_datadir}/%{name}/ukrainian
%{_datadir}/%{name}/charsets

%files server
%defattr(-,root,root)
%doc support-files/*.cnf

%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions
%{_bindir}/mysql_install_db
%{_bindir}/mysql_plugin
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%ghost %{_bindir}/mysqlbug
%{_bindir}/mysqldumpslow
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mysqltest
%{_bindir}/innochecksum
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolve_stack_dump
%{_bindir}/resolveip

%config(noreplace) %{_sysconfdir}/my.cnf.d/server.cnf
%{?with_tokudb:%config(noreplace) %{_sysconfdir}/my.cnf.d/tokudb.cnf}

%{_libexecdir}/mysqld

%{_libdir}/mysql/INFO_SRC
%{_libdir}/mysql/INFO_BIN

%{_libdir}/mysql/mysqlbug

%{_libdir}/mysql/plugin

%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man8/mysqld.8*

%{_datadir}/%{name}/errmsg-utf8.txt
%{_datadir}/%{name}/fill_help_tables.sql
%{_datadir}/%{name}/mysql_system_tables.sql
%{_datadir}/%{name}/mysql_system_tables_data.sql
%{_datadir}/%{name}/mysql_test_data_timezone.sql
%{_datadir}/%{name}/mysql_performance_tables.sql
%{_datadir}/mysql/my-*.cnf
%{_datadir}/mysql/config.*.ini

%{_sysconfdir}/rc.d/init.d/mysqld

%attr(0755,mysql,mysql) %dir %{_localstatedir}/run/mysqld
%attr(0755,mysql,mysql) %dir %{_localstatedir}/lib/mysql
%attr(0640,mysql,mysql) %config(noreplace) %verify(not md5 size mtime) %{_localstatedir}/log/mysqld.log
%config(noreplace) %{_sysconfdir}/logrotate.d/mysqld

%files devel
%defattr(-,root,root)
%{_includedir}/mysql
%{_datadir}/aclocal/mysql.m4
%{_libdir}/mysql/libmysqlclient.so
%{_libdir}/mysql/libmysqlclient_r.so

%files embedded
%defattr(-,root,root)
%doc README COPYING COPYING.LESSER README.mysql-license
%doc storage/innobase/COPYING.Percona storage/innobase/COPYING.Google
%{_libdir}/mysql/libmysqld.so.*

%files embedded-devel
%defattr(-,root,root)
%{_libdir}/mysql/libmysqld.so
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest_embedded.1*

%files bench
%defattr(-,root,root)
%{_datadir}/sql-bench

%files test
%defattr(-,root,root)
%{_bindir}/mysql_client_test
%{_bindir}/my_safe_process
%attr(-,mysql,mysql) %{_datadir}/mysql-test

%{_mandir}/man1/mysql_client_test.1*

%changelog
* Thu Nov 21 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-6
- Disable PIE, it doesn't seem to work fine in RHEL-5

* Tue Nov 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-5
- Merge couple of changes from Fedora Rawhide

* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-4
- Fix spec file to be ready for backport by Oden Eriksson
  Resolves: #1026404

* Mon Nov  4 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-3
- Add pam-devel to build-requires in order to build
  Related: #1019945
- Check if correct process is running in mysql-wait-ready script
  Related: #1026313

* Mon Oct 14 2013 Honza Horak <hhorak@redhat.com> 1:5.5.33a-2
- Turn on test suite

* Mon Sep  2 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-12
- Re-organize my.cnf to include only generic settings
  Resolves: #1003115
- Move pid file location to /var/run/mariadb
- Make mysqld a symlink to mariadb unit file rather than the opposite way
  Related: #999589

* Thu Aug 29 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-11
- Move log file into /var/log/mariadb/mariadb.log
- Rename logrotate script to mariadb
- Resolves: #999589

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1:5.5.32-10
- fix alternatives usage

* Tue Aug 13 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-9
- Multilib issues solved by alternatives
  Resolves: #986959

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.32-8
- Perl 5.18 rebuild

* Wed Jul 31 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-7
- Do not use login shell for mysql user

* Tue Jul 30 2013 Honza Horak <hhorak@redhat.com> - 1:5.5.32-6
- Remove unneeded systemd-sysv requires
- Provide mysql-compat-server symbol
- Create mariadb.service symlink
- Fix multilib header location for arm
- Enhance documentation in the unit file
- Use scriptstub instead of links to avoid multilib conflicts
- Add condition for doc placement in F20+

* Sun Jul 28 2013 Dennis Gilmore <dennis@ausil.us> - 1:5.5.32-5
- remove "Requires(pretrans): systemd" since its not possible
- when installing mariadb and systemd at the same time. as in a new install

* Sat Jul 27 2013 Kevin Fenzi <kevin@scrye.com> 1:5.5.32-4
- Set rpm doc macro to install docs in unversioned dir

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> 1:5.5.32-3
- add Requires(pre) on systemd for the server package

* Tue Jul 23 2013 Dennis Gilmore <dennis@ausil.us> 1:5.5.32-2
- replace systemd-units requires with systemd
- remove solaris files

* Fri Jul 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.32-1
- Rebase to 5.5.32
  https://kb.askmonty.org/en/mariadb-5532-changelog/
- Clean-up un-necessary systemd snippets

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:5.5.31-7
- Perl 5.18 rebuild

* Mon Jul  1 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-6
- Test suite params enhanced to decrease server condition influence
- Fix misleading error message when uninstalling built-in plugins
  Related: #966873

* Thu Jun 27 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-5
- Apply fixes found by Coverity static analysis tool

* Wed Jun 19 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-4
- Do not use pretrans scriptlet, which doesn't work in anaconda
  Resolves: #975348

* Fri Jun 14 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-3
- Explicitly enable mysqld if it was enabled in the beggining
  of the transaction.

* Thu Jun 13 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-2
- Apply man page fix from Jan Stanek

* Fri May 24 2013 Honza Horak <hhorak@redhat.com> 1:5.5.31-1
- Rebase to 5.5.31
  https://kb.askmonty.org/en/mariadb-5531-changelog/
- Preserve time-stamps in case of installed files
- Use /var/tmp instead of /tmp, since the later is using tmpfs,
  which can cause problems
  Resolves: #962087
- Fix test suite requirements

* Sun May  5 2013 Honza Horak <hhorak@redhat.com> 1:5.5.30-2
- Remove mytop utility, which is packaged separately
- Resolve multilib conflicts in mysql/private/config.h

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.30-1
- Rebase to 5.5.30
  https://kb.askmonty.org/en/mariadb-5530-changelog/

* Fri Mar 22 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-11
- Obsolete MySQL since it is now renamed to community-mysql
- Remove real- virtual names

* Thu Mar 21 2013 Honza Horak <hhorak@redhat.com> 1:5.5.29-10
- Adding epoch to have higher priority than other mysql implementations
  when comes to provider comparison

* Wed Mar 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-9
- Let mariadb-embedded-devel conflict with MySQL-embedded-devel
- Adjust mariadb-sortbuffer.patch to correspond with upstream patch

* Mon Mar  4 2013 Honza Horak <hhorak@redhat.com> 5.5.29-8
- Mask expected warnings about setrlimit in test suite

* Thu Feb 28 2013 Honza Horak <hhorak@redhat.com> 5.5.29-7
- Use configured prefix value instead of guessing basedir
  in mysql_config
Resolves: #916189
- Export dynamic columns and non-blocking API functions documented
  by upstream

* Wed Feb 27 2013 Honza Horak <hhorak@redhat.com> 5.5.29-6
- Fix sort_buffer_length option type

* Wed Feb 13 2013 Honza Horak <hhorak@redhat.com> 5.5.29-5
- Suppress warnings in tests and skip tests also on ppc64p7

* Tue Feb 12 2013 Honza Horak <hhorak@redhat.com> 5.5.29-4
- Suppress warning in tests on ppc
- Enable fixed index_merge_myisam test case

* Thu Feb 07 2013 Honza Horak <hhorak@redhat.com> 5.5.29-3
- Packages need to provide also %%_isa version of mysql package
- Provide own symbols with real- prefix to distinguish from mysql
  unambiguously
- Fix format for buffer size in error messages (MDEV-4156)
- Disable some tests that fail on ppc and s390
- Conflict only with real-mysql, otherwise mariadb conflicts with ourself

* Tue Feb 05 2013 Honza Horak <hhorak@redhat.com> 5.5.29-2
- Let mariadb-libs to own /etc/my.cnf.d

* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.29-1
- Rebase to 5.5.29
  https://kb.askmonty.org/en/mariadb-5529-changelog/
- Fix inaccurate default for socket location in mysqld-wait-ready
  Resolves: #890535

* Thu Jan 31 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-8
- Enable obsoleting mysql

* Wed Jan 30 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-7
- Adding necessary hacks for perl dependency checking, rpm is still
  not wise enough
- Namespace sanity re-added for symbol default_charset_info

* Mon Jan 28 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-6
- Removed %%{_isa} from provides/obsoletes, which doesn't allow
  proper obsoleting
- Do not obsolete mysql at the time of testing

* Thu Jan 10 2013 Honza Horak <hhorak@redhat.com> 5.5.28a-5
- Added licenses LGPLv2 and BSD
- Removed wrong usage of %%{epoch}
- Test-suite is run in %%check
- Removed perl dependency checking adjustment, rpm seems to be smart enough
- Other minor spec file fixes

* Tue Dec 18 2012 Honza Horak <hhorak@redhat.com> 5.5.28a-4
- Packaging of MariaDB based on MySQL package

