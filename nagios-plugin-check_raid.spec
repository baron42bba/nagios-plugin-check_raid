%if %(test -f /etc/redhat-release && echo 1 || echo 0 )
%define target redhat
%else
%define target unknown
%endif
%define		plugin	check_raid
Summary:	Nagios plugin to check current server's RAID status
%if %{target} == "redhat"
Name:		nagios-plugins-%{plugin}
%else
Name:		nagios-plugin-%{plugin}
%endif
Version:	%{version}
Release:	%{release}
License:	GPL v2
Group:		Networking
Source0:	%{plugin}.pl
Source1:	%{plugin}.cfg
URL:		https://github.com/glensc/nagios-plugin-check_raid
Requires:	/usr/bin/perl
Requires:	sudo
%if %{target} != "redhat"
Suggests:	CmdTool2
Suggests:	arcconf
Suggests:	areca-cli
Suggests:	cciss_vol_status
Suggests:	hpacucli
Suggests:	lsscsi
Suggests:	megacli-sas
Suggests:	megarc-scsi
Suggests:	mpt-status
Suggests:	smartmontools
Suggests:	tw_cli-9xxx
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%if %{target} == "redhat"
%define		docdir          %{_prefix}/share/doc/%{name}-%{version}
%else
%define		docdir          %{_prefix}/share/doc/%{name}-%{version}
%endif

%description
This plugin checks Check all RAID volumes (hardware and software) that
can be identified.

Supports:
- AIX software RAID via lsvg
- Adaptec AAC RAID via aaccli or afacli or arcconf
- Areca SATA RAID Support
- HP Smart Array (MSA1500) via serial line
- HP Smart Array Controllers and MSA Controllers via hpacucli (see
  hapacucli readme)
- HP/Compaq Smart Array via cciss_vol_status (hpsa supported too)
- LSI Logic MegaRAID SAS series via MegaCli
- LSI MegaRaid via lsraid
- Linux 3ware SATA RAID via tw_cli
- Linux DPT/I2O hardware RAID controllers via /proc/scsi/dpt_i2o
- Linux GDTH hardware RAID controllers via /proc/scsi/gdth
- Linux LSI MegaRaid hardware RAID via /proc/megaraid
- Linux LSI MegaRaid hardware RAID via CmdTool2
- Linux LSI MegaRaid hardware RAID via megarc
- Linux MPT hardware RAID via mpt-status
- Linux MegaIDE hardware RAID controllers via /proc/megaide
- Linux software RAID (md) via /proc/mdstat
- SAS2IRCU support
- Serveraid IPS via ipssend
- Solaris software RAID via metastat

%prep
%setup -qcT
cp -p %{SOURCE0} .
cp -p %{_sourcedir}/README.md .
cp -p %{_sourcedir}/ChangeLog.md .
cp -p %{_sourcedir}/CONTRIBUTING.md .
cp -p %{SOURCE1} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir},%{docdir}}
install -p %{plugin}.pl $RPM_BUILD_ROOT%{plugindir}/%{plugin}
install -p %{plugin}.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg
install -p README.md $RPM_BUILD_ROOT%{docdir}/README.md
install -p ChangeLog.md $RPM_BUILD_ROOT%{docdir}/ChangeLog.md
install -p CONTRIBUTING.md $RPM_BUILD_ROOT%{docdir}/CONTRIBUTING.md

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = 1 ]; then
	# setup sudo rules on first install
	%{plugindir}/%{plugin} -S || :
fi

%postun
if [ "$1" = 0 ]; then
	# remove all sudo rules related to us
	%{__sed} -i -e '/CHECK_RAID/d' /etc/sudoers
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
%attr(644,root,root) %{docdir}/*
