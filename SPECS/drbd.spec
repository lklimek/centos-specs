%kmdl drbd

Summary: Distributed Replicated Block Device.
Name: drbd
Version: 8.4.4
Release: 33%{?dist}
License: GPLv2
Group: System Environment/Kernel
URL: http://www.drbd.org/
Source0: http://oss.linbit.com/drbd/8.4/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: bison, m4, flex
BuildRequires: /etc/redhat-release
BuildRequires: udev
%kmdl_parentdependencies
# Compatibilty with the Fedora import
Provides: drbd-utils = %{evr}, drbd-xen = %{evr}, drbd-udev = %{evr}
Provides: drbd-pacemaker = %{evr}, drbd-rgmanager = %{evr}
Provides: drbd-heartbeat = %{evr}, drbd-bash-completion = %{evr}
Obsoletes: drbd-utils < %{evr}, drbd-xen < %{evr}, drbd-udev < %{evr}
Obsoletes: drbd-pacemaker < %{evr}, drbd-rgmanager < %{evr}
Obsoletes: drbd-heartbeat < %{evr}, drbd-bash-completion < %{evr}

%description
DRBD is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network raid-1.

%package -n %kmdl_name
%kmdl_dependencies
Summary: Distributed Redundant Block Device.
Group: System Environment/Kernel

%description -n %kmdl_name
DRBD is a block device which is designed to build high availability
clusters. This is done by mirroring a whole block device via (a
dedicated) network. You could see it as a network raid-1.

%kmdl_desc

%prep
%setup -q
grep gfp_t %{kmdl_kernelsrcdir}/include/linux/gfp.h > /dev/null \
  && perl -pi -e's,(.* gfp_t;)$,/* $1 */,' drbd/drbd_wrappers.h

%build
%if %{kmdl_userland}
%configure
#make SUBDIRS="user documentation scripts benchmark" KDIR=%{kmdl_kernelsrcdir}
make

%else
%configure --with-km KDIR=%{kmdl_kernelsrcdir}
cd drbd
#make clean
make KDIR=%{kmdl_kernelsrcdir}

%endif

%install
rm -rf %{buildroot}
%if %{kmdl_userland}

make install DESTDIR=%{buildroot}
#make install SUBDIRS="user documentation scripts benchmark" PREFIX=%{buildroot} KVER=dummy DRBD_ENABLE_UDEV=sure

%else
mkdir -p %{buildroot}%{kmdl_moduledir}/drivers/block
cd drbd
make install KDIR=%{kmdl_kernelsrcdir} DESTDIR=%{buildroot}
#make KDIR=%{kmdl_kernelsrcdir} PREFIX=%{buildroot} install
#mv %{buildroot}%{kmdl_moduledir}/../kernel/drivers/block/* %{buildroot}%{kmdl_moduledir}/drivers/block/

%endif

%clean
rm -rf %{buildroot}

%post -n %kmdl_name
%kmdl_install

%postun -n %kmdl_name
%kmdl_remove

%if %{kmdl_userland}

%files
%defattr(-,root,root,-)
%doc README* ChangeLog COPYING
%dir %{_sysconfdir}/drbd.d
%config(noreplace) %{_sysconfdir}/drbd.d/global_common.conf
%config(noreplace) %{_sysconfdir}/drbd.conf
%config(noreplace) %{_sysconfdir}/xen/scripts/block-drbd
%{_initdir}/drbd
%config(noreplace) %{_sysconfdir}/ha.d/resource.d/drbddisk
%config(noreplace) %{_sysconfdir}/ha.d/resource.d/drbdupper
%config(noreplace) %{_sysconfdir}/udev/rules.d/65-drbd.rules*
/sbin/drbdsetup
/sbin/drbdadm
/sbin/drbdmeta
%{_sbindir}/drbd-overview
#%{_libdir}/drbd
/usr/lib/drbd
#%{_datadir}/cluster
%{_mandir}/man8/drbdadm.8*
%{_mandir}/man5/drbd.conf.5*
%{_mandir}/man8/drbddisk.8*
%{_mandir}/man8/drbd.8*
%{_mandir}/man8/drbdsetup.8*
%{_mandir}/man8/drbdmeta.8*
/usr/lib/ocf
%{_sysconfdir}/bash_completion.d
/lib/drbd/drbdadm-83
/lib/drbd/drbdsetup-83

%else

%files -n %kmdl_name
%defattr(-,root,root,-)
%{kmdl_moduledir}

%endif

%changelog
* Mon May 13 2013 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.4.3-33
- update to 8.4.3.

* Thu May 24 2012 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.4.1-32
- Update to 8.4.1.

* Fri Aug 26 2011 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.4.0-31
- Update to 8.4.0.

* Sun Oct 10 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.3.8.1-30
- Update to 8.3.8.1.

* Sat Jun  5 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.3.8-29
- Update to 8.3.8.

* Sat Apr 24 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.3.7-28
- Update to 8.3.7.

* Sun Nov 29 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.3.6-27
- Update to 8.3.6.

* Tue Sep  8 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.3.2-25
- Update to 8.3.2.

* Mon Apr 20 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.3.1-24
- Update to 8.3.1.

* Sun Dec  7 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.2.7-23
- Update to 8.2.7.

* Fri Oct  3 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.2.6-22
- Update to 8.2.6.

* Sat Mar 22 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.2.5-21
- Update to 8.2.5.

* Fri Nov 23 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.2.1-20
- Update to 8.2.1.

* Tue Jul 31 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 8.0.4-18
- Update to 8.0.4.

* Tue Jul 31 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.24-17
- Update to 0.7.24.

* Sat Jan 13 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.23-15
- Update to 0.7.23.
- Fix summary (#1110).

* Tue Jan  2 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.22-14
- Update to 0.7.22.

* Sun Oct 22 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.21-13
- Update to 0.7.21.

* Mon Jul 17 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.7.20-12
- Update to 0.7.20.

* Sat Mar 25 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.17.

* Tue Mar  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.16.

* Tue Jul 12 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.11.

* Thu Apr 21 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.10.

* Sun Jan 23 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.8.

* Wed Jan 12 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.7.

* Sun Oct  3 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.7.5.

* Sat Jun 19 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.

