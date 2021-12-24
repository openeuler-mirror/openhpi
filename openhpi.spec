Name:                openhpi
Version:             3.8.0
Release:             9
Summary:             Implementation of the Service Availability Forum's Hardware Platform Interface
License:             BSD
URL:                 http://www.openhpi.org
Source0:             https://github.com/open-hpi/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:              openhpi-3.4.0-systemd.patch
Patch1:              openhpi-3.6.1-ssl.patch

BuildRequires:       glib2-devel gcc-c++ libsysfs-devel net-snmp-devel OpenIPMI-devel libtool-ltdl-devel
BuildRequires:       openssl-devel ncurses-devel libxml2-devel docbook-utils libuuid-devel librabbitmq-devel
BuildRequires:       json-c-devel libcurl-devel systemd autoconf automake libtool libgcrypt-devel
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd
Provides:            openhpi-libs = %{version}-%{release}
Provides:            openhpi-libs%{?_isa} = %{version}-%{release}
Obsoletes:           openhpi-libs < %{version}-%{release}

%description
OpenHPI provides an open source implementation of the Service Availability
Forum (SAF) Hardware Platform Interface (HPI). HPI is an abstracted interface
for managing computer hardware, typically chassis and rack based servers. HPI
includes resource modeling; access to and control over sensor, control,
watchdog, and inventory data associated with resources; abstracted System
Event Log interfaces; hardware events and alarms; and a managed hotswap
interface.

OpenHPI's architecture contains a modular mechanism intended to make adding
new hardware support easier. Several plugins exist in the OpenHPI source tree
giving access to various types of hardware. This includes, but is not limited
to, IPMI based servers, Blade Center, and machines which export data via sysfs.

%package devel
Summary:             Development files for openhpi
Requires:            %{name}%{?_isa} = %{version}-%{release}
Requires:            glib2-devel

%description devel
This package contains libraries and headier files for developing applications
that use openhpi.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1
autoreconf -ivf

chmod a-x plugins/simulator/*.[ch]
chmod a-x clients/hpipower.c

if [ $UID -eq 0 ]; then
    find . -name openhpi.conf -exec chown root:root {} \;
    find . -name openhpi.conf -execdir chown root:root . \;
fi

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
%configure --disable-static --with-systemdsystemunitdir=%{_unitdir}

%disable_rpath

make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p -m1755 $RPM_BUILD_ROOT%{_var}/lib/%{name}
%make_install

%delete_la

%check
make check

%post
%systemd_post openhpid.service

%preun
%systemd_preun openhpid.service

%postun
%systemd_postun_with_restart openhpid.service

%files
%defattr(-,root,root)
%license %{_docdir}/%{name}/COPYING
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}client.conf
%config(noreplace) %{_sysconfdir}/%{name}/simulation.data
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{name}
%{_libdir}/*.so.*
%{_unitdir}/openhpid.service
%dir %{_sysconfdir}/%{name}
%attr(1755,root,root) %{_var}/lib/%{name}

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc

%files help
%defattr(-,root,root)
%doc %{_docdir}/%{name}/ChangeLog 
%doc %{_docdir}/%{name}/README*
%{_mandir}/man1/*1*
%{_mandir}/man7/*7*
%{_mandir}/man8/*8*

%changelog
* Wed Dec 22 2021 liyanan <liyanan32@huawei.com> - 3.8.0-9
- fix update error

* Tue Sep 15 2020 Ge Wang <wangge20@huawei.com> - 3.8.0-7
- Modify Source0 Url

* Tue Nov 26 2019 openEuler Buildteam <buildteam@openeuler.org> - 3.8.0-6
- Package init
